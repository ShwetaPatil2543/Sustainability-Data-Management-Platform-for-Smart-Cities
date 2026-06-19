import os
import sys
import django
import traceback

# ensure project root is on path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sustainability_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate
from reports.views import SustainabilityReportViewSet

User = get_user_model()

u, created = User.objects.get_or_create(username='sdmp_test')
if created:
    u.set_password('testpass123')
    u.is_staff = True
    u.is_superuser = True
    u.save()

factory = APIRequestFactory()
req = factory.get('/api/reports/pdf/')
force_authenticate(req, user=u)

try:
    view = SustainabilityReportViewSet.as_view({'get': 'download_pdf'})
    resp = view(req)
    print('STATUS', getattr(resp, 'status_code', None))
    if hasattr(resp, 'data'):
        print('DATA', resp.data)
    else:
        print('RESPONSE', resp)
except Exception:
    print('EXCEPTION')
    traceback.print_exc()
