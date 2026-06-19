# Reports app — persistence & migration note

This small app provides export endpoints for sustainability reports used by the frontend:

- `GET /api/reports/pdf/` — download PDF report
- `GET /api/reports/csv/` — download CSV report

Important notes for local development
0. Install Python dependencies (including `reportlab`) from the project `requirements.txt`:

```bash
pip install -r requirements.txt
```

1. The `reports` app requires a database table (`reports_sustainabilityreport`) to exist for the viewset to iterate stored reports. If you see a 500 error mentioning `no such table: reports_sustainabilityreport` run the migrations below.

Apply migrations:

```bash
cd sustainability_backend
python manage.py makemigrations reports
python manage.py migrate reports
```

2. If you prefer not to store reports yet, the endpoints will now gracefully return an empty PDF/CSV when no rows exist. This was added to avoid 500s during early development.

3. To persist sample reports for testing, use the Django admin or a small data script (example below):

```python
from reports.models import SustainabilityReport
SustainabilityReport.objects.create(industry='Demo', department='Ops', date='2026-03-01', total_emission=123.45)
```

4. If you plan to run these endpoints from a browser (frontend), ensure the backend is reachable at the URL configured in the frontend's `VITE_API_BASE_URL` (defaults to `http://127.0.0.1:8000/api`).

If you want, I can also add a management command to seed demo reports automatically.
