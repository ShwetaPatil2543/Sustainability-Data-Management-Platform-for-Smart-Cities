from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from industries.models import Industry
from emissions.models import CarbonEmission
from energy.models import EnergyUsage
from fuel.models import FuelConsumption
from air_quality.models import AirQuality

from django.db.models import Sum, Avg
from datetime import timedelta
from users.decorators import role_required  # <- import decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ai_engine.predictor import SustainabilityPredictor
from ai_engine.scorer import classify_alerts
from ai_engine.recommender import Recommender, generate_recommendations_from_alerts

# ---------------------------
# API view for dashboard stats
# ---------------------------
class DashboardStatsView(APIView):
    def get(self, request):
        total_industries = Industry.objects.count()

        total_emissions = CarbonEmission.objects.aggregate(
            total=Sum("total_emission")
        )["total"]

        total_energy = EnergyUsage.objects.aggregate(
            total=Sum("total_energy")
        )["total"]

        total_fuel = FuelConsumption.objects.aggregate(
            total=Sum("quantity")
        )["total"]

        avg_aqi = AirQuality.objects.aggregate(
            avg=Avg("aqi")
        )["avg"]

        data = {
            "total_industries": total_industries,
            "total_emissions": total_emissions,
            "total_energy": total_energy,
            "total_fuel": total_fuel,
            "average_aqi": avg_aqi,
        }

        return Response(data)


class SmartDashboardView(APIView):
    """Combined smart dashboard API that aggregates metrics, predictions, alerts and recommendations."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # totals
        total_emission = CarbonEmission.objects.aggregate(
            co2_sum=Sum('co2_emission'), methane_sum=Sum('methane_emission'), nitro_sum=Sum('nitrous_oxide')
        )
        total_emission_value = (total_emission.get('co2_sum') or 0) + (total_emission.get('methane_sum') or 0) + (total_emission.get('nitro_sum') or 0)

        # emission chart (last 30 days)
        from django.utils import timezone
        today = timezone.now().date()
        start = today - timedelta(days=29)

        emissions_qs = (
            CarbonEmission.objects
            .filter(date__range=[start, today])
            .values('date')
            .annotate(co2_sum=Sum('co2_emission'), methane_sum=Sum('methane_emission'), nitro_sum=Sum('nitrous_oxide'))
            .order_by('date')
        )
        emission_chart = []
        for r in emissions_qs:
            total = (r.get('co2_sum') or 0) + (r.get('methane_sum') or 0) + (r.get('nitro_sum') or 0)
            emission_chart.append({'date': r['date'].isoformat(), 'value': round(float(total), 2)})

        # predictions
        predictor = SustainabilityPredictor()
        predictions = predictor.get_predictions(days=7)

        # latest metrics for alerts
        latest_em = (
            CarbonEmission.objects.order_by('-date')
            .values('date')
            .annotate(co2_sum=Sum('co2_emission'), methane_sum=Sum('methane_emission'), nitro_sum=Sum('nitrous_oxide'))
            .first()
        )
        latest_em_value = 0
        if latest_em:
            latest_em_value = (latest_em.get('co2_sum') or 0) + (latest_em.get('methane_sum') or 0) + (latest_em.get('nitro_sum') or 0)

        latest_aqi_obj = AirQuality.objects.order_by('-date').first()
        latest_aqi = latest_aqi_obj.aqi if latest_aqi_obj else None

        latest_energy_obj = EnergyUsage.objects.order_by('-date').first()
        latest_energy = latest_energy_obj.total_energy if latest_energy_obj else None

        alerts = classify_alerts(emission=latest_em_value, aqi=latest_aqi, energy=latest_energy)

        # recommendations
        recommender = Recommender()
        recommendations = recommender.get_recommendations(days=30)
        # also include alert-based short recs
        recommendations = generate_recommendations_from_alerts(alerts) + recommendations

        # industry comparison
        industry_qs = (
            CarbonEmission.objects
            .values('industry__name')
            .annotate(co2_sum=Sum('co2_emission'), methane_sum=Sum('methane_emission'), nitro_sum=Sum('nitrous_oxide'))
            .order_by('-co2_sum')
        )
        industry_comparison = []
        for r in industry_qs:
            total = (r.get('co2_sum') or 0) + (r.get('methane_sum') or 0) + (r.get('nitro_sum') or 0)
            industry_comparison.append({'industry': r.get('industry__name') or 'Unknown', 'value': round(float(total), 2)})

        response = {
            'total_emission': round(float(total_emission_value), 2),
            'emission_chart': emission_chart,
            'prediction': predictions,
            'alerts': alerts,
            'recommendations': recommendations,
            'industry_comparison': industry_comparison,
        }

        return Response(response, status=status.HTTP_200_OK)


# ---------------------------
# RBAC-protected template views
# ---------------------------

# Admin-only dashboard
@role_required('Admin')
def admin_dashboard(request):
    return render(request, 'dashboard/admin.html')


# Admin + Manager dashboard
@role_required('Admin', 'Manager')
def manager_dashboard(request):
    return render(request, 'dashboard/manager.html')


# Admin + Manager + Analyst dashboard
@role_required('Admin', 'Manager', 'Analyst')
def analyst_dashboard(request):
    return render(request, 'dashboard/analyst.html')