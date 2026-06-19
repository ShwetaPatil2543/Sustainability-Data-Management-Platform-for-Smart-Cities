from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import FuelConsumption
from .serializers import FuelConsumptionSerializer
import pandas as pd


class FuelConsumptionViewSet(viewsets.ModelViewSet):

    queryset = FuelConsumption.objects.all().order_by("date")
    serializer_class = FuelConsumptionSerializer
    permission_classes = [IsAuthenticated]


class FuelUploadView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        try:

            # Read file
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)

            elif file.name.endswith((".xlsx", ".xls")):
                df = pd.read_excel(file)

            else:
                return Response({"error": "Unsupported format"}, status=400)

            created = 0

            for _, row in df.iterrows():

                # Safe value reading
                quantity = float(row.get("fuel_amount", 0))
                emission_factor = float(row.get("emission_factor", 0))
                cost = float(row.get("cost", 0))

                # Fix fuel type formatting
                fuel_type = str(row.get("fuel_type", "")).strip().title()

                if fuel_type.lower() == "gas":
                    fuel_type = "Natural Gas"

                fuel_data = {

                    "industry": row.get("industry"),
                    "department": row.get("department"),
                    "date": row.get("date"),
                    "fuel_type": fuel_type,
                    "quantity": quantity,
                    "carbon_emission_factor": emission_factor,
                    "cost": cost,
                    "total_emission": quantity * emission_factor

                }

                serializer = FuelConsumptionSerializer(data=fuel_data)

                if serializer.is_valid():
                    serializer.save()
                    created += 1

            return Response({
                "message": "Upload successful",
                "records_created": created
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)