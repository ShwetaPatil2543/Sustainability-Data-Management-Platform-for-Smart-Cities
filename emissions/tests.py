from django.test import TestCase
from django.core.management import call_command
from datetime import date, timedelta

from industries.models import Industry
from .models import CarbonEmission
from .serializers import CarbonEmissionSerializer


class CarbonEmissionModelTest(TestCase):
	def setUp(self):
		self.ind = Industry.objects.create(name='Test Industry', location='Nowhere')

	def test_save_populates_total_if_missing(self):
		ce = CarbonEmission.objects.create(
			industry=self.ind,
			date=date(2020, 1, 1),
			co2_emission=10.0,
			methane_emission=1.0,
			nitrous_oxide=0.5,
		)
		self.assertIsNotNone(ce.total_emission)
		self.assertAlmostEqual(ce.total_emission, 11.5)

	def test_backfill_command_sets_missing_totals(self):
		# Create a record then force total_emission to NULL to simulate older data
		ce = CarbonEmission.objects.create(
			industry=self.ind,
			date=date(2020, 2, 1),
			co2_emission=5.0,
			methane_emission=0.5,
			nitrous_oxide=0.2,
		)
		# Null out the stored value as if created before migration
		CarbonEmission.objects.filter(id=ce.id).update(total_emission=None)
		ce.refresh_from_db()
		self.assertIsNone(ce.total_emission)

		# Run backfill
		call_command('backfill_total_emission', batch_size=50)
		ce.refresh_from_db()
		self.assertIsNotNone(ce.total_emission)
		self.assertAlmostEqual(ce.total_emission, 5.7)


class CarbonEmissionSerializerTest(TestCase):
	def setUp(self):
		self.ind = Industry.objects.create(name='SerTest', location='Here')

	def test_future_date_rejected_unless_predicted(self):
		future = (date.today() + timedelta(days=10)).isoformat()
		data = {
			'industry': self.ind.id,
			'date': future,
			'co2_emission': 1.0,
			'methane_emission': 0.0,
			'nitrous_emission': 0.0,
		}
		ser = CarbonEmissionSerializer(data=data)
		self.assertFalse(ser.is_valid())
		self.assertIn('date', ser.errors)

		# If source is predicted, allow future date
		data['source'] = 'predicted'
		ser2 = CarbonEmissionSerializer(data=data)
		self.assertTrue(ser2.is_valid(), msg=str(ser2.errors))


class CarbonEmissionAnalyticsTest(TestCase):
	def setUp(self):
		from django.contrib.auth import get_user_model
		User = get_user_model()
		self.user = User.objects.create(username='tester')
		self.client.force_login(self.user)
		self.ind1 = Industry.objects.create(name='Ind A', location='L')
		self.ind2 = Industry.objects.create(name='Ind B', location='L')
		# create data across two months
		CarbonEmission.objects.create(industry=self.ind1, date='2023-01-10', co2_emission=10, methane_emission=1, nitrous_oxide=0)
		CarbonEmission.objects.create(industry=self.ind1, date='2023-02-12', co2_emission=20, methane_emission=2, nitrous_oxide=0)
		CarbonEmission.objects.create(industry=self.ind2, date='2023-02-15', co2_emission=5, methane_emission=0.5, nitrous_oxide=0)

	def test_aggregates_endpoint(self):
		client = self.client
		resp = client.get('/emissions/aggregates/')
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertIn('total', data)
		self.assertGreaterEqual(data['total'], 0)

	def test_trends_grouping(self):
		client = self.client
		resp = client.get('/emissions/trends/?group=monthly')
		self.assertEqual(resp.status_code, 200)
		arr = resp.json()
		self.assertIsInstance(arr, list)

	def test_top_emitters(self):
		client = self.client
		resp = client.get('/emissions/top-emitters/?limit=2')
		self.assertEqual(resp.status_code, 200)
		arr = resp.json()
		self.assertLessEqual(len(arr), 2)

	def test_json_bulk_upload_dry_run(self):
		payload = [
			{'industry': self.ind1.id, 'date': '2023-03-01', 'co2_emission': 1.0, 'methane_emission': 0.0},
			{'industry': self.ind2.id, 'date': '2023-03-02', 'co2_emission': 2.0, 'methane_emission': 0.0},
		]
		resp = self.client.post('/emissions/bulk-upload/?dry_run=true', data=payload, content_type='application/json')
		self.assertIn(resp.status_code, (200, 201))
		data = resp.json()
		self.assertEqual(data.get('created'), 2)

	def test_json_bulk_upload_create(self):
		payload = [
			{'industry': self.ind1.id, 'date': '2023-04-01', 'co2_emission': 3.0, 'methane_emission': 0.0},
		]
		resp = self.client.post('/emissions/bulk-upload/', data=payload, content_type='application/json')
		self.assertIn(resp.status_code, (200, 201))
		data = resp.json()
		self.assertEqual(data.get('created'), 1)

	def test_idempotency_key_prevents_duplicate(self):
		payload = [
			{'industry': self.ind1.id, 'date': '2023-05-01', 'co2_emission': 1.5, 'methane_emission': 0.0},
		]
		headers = {'HTTP_IDEMPOTENCY_KEY': 'abc-123'}
		resp1 = self.client.post('/emissions/bulk-upload/', data=payload, content_type='application/json', **headers)
		self.assertIn(resp1.status_code, (200, 201))
		resp2 = self.client.post('/emissions/bulk-upload/', data=payload, content_type='application/json', **headers)
		self.assertEqual(resp2.status_code, 200)
		self.assertIn('message', resp2.json())
