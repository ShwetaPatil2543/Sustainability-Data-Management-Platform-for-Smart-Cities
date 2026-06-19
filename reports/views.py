from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http import HttpResponse
import csv
try:
    from reportlab.pdfgen import canvas
except ImportError:
    canvas = None

from .models import SustainabilityReport
from django.db import utils as db_utils
from .serializers import SustainabilityReportSerializer


class SustainabilityReportViewSet(ModelViewSet):

    queryset = SustainabilityReport.objects.all()
    serializer_class = SustainabilityReportSerializer
    permission_classes = [IsAuthenticated]

    # ---------------- CSV DOWNLOAD ----------------
    @action(detail=False, methods=['get'], url_path='csv')
    def download_csv(self, request):

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="sustainability_report.csv"'

        writer = csv.writer(response)

        writer.writerow([
            "ID",
            "Industry",
            "Department",
            "Date",
            "Total Emission"
        ])

        try:
            reports = list(SustainabilityReport.objects.all())
        except db_utils.OperationalError:
            reports = []

        for r in reports:

            writer.writerow([
                r.id,
                r.industry,
                r.department,
                r.date,
                r.total_emission
            ])

        return response


    # ---------------- PDF DOWNLOAD ----------------
    @action(detail=False, methods=['get'], url_path='pdf')
    def download_pdf(self, request):
        if canvas is None:
            return HttpResponse(
                "PDF generation requires the 'reportlab' package. Install it with: pip install reportlab",
                status=501,
                content_type="text/plain",
            )

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="sustainability_report.pdf"'

        pdf = canvas.Canvas(response)
        pdf.setFont("Helvetica", 14)
        pdf.drawString(200, 800, "Sustainability Report")

        y = 760

        try:
            reports = list(SustainabilityReport.objects.all())
        except db_utils.OperationalError:
            reports = []

        for r in reports:
            line = f"ID: {r.id} | Industry: {r.industry} | Emission: {r.total_emission}"
            pdf.drawString(50, y, line)
            y -= 25
            if y < 50:
                pdf.showPage()
                y = 800

        pdf.save()
        return response