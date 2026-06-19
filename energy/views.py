from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import EnergyUsage
from .serializers import EnergyUsageSerializer
import pandas as pd

class EnergyUsageViewSet(viewsets.ModelViewSet):
    queryset = EnergyUsage.objects.all().order_by("date")
    serializer_class = EnergyUsageSerializer
    permission_classes = [IsAuthenticated]


class EnergyUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        try:
            # Read the file based on extension
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                return Response({"error": "Unsupported file format. Use CSV or Excel."}, status=400)

            # Validate required columns
            required_columns = ['industry', 'department', 'date', 'electricity_consumption', 'renewable_energy', 'non_renewable_energy']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response({"error": f"Missing required columns: {missing_columns}"}, status=400)

            # Process each row
            created = []
            errors = []

            for idx, row in df.iterrows():
                try:
                    # Convert date if needed
                    date_value = pd.to_datetime(row['date']).date()

                    # Get or create industry and department
                    from industries.models import Industry, Department
                    industry, _ = Industry.objects.get_or_create(name=str(row['industry']))
                    department, _ = Department.objects.get_or_create(
                        name=str(row['department']),
                        defaults={'industry': industry}
                    )

                    # Create energy usage record
                    energy_data = {
                        'industry': industry.id,
                        'department': department.id,
                        'date': date_value,
                        'electricity_consumption': float(row['electricity_consumption']),
                        'renewable_energy': float(row['renewable_energy']),
                        'non_renewable_energy': float(row['non_renewable_energy']),
                    }

                    serializer = EnergyUsageSerializer(data=energy_data)
                    if serializer.is_valid():
                        serializer.save()
                        created.append(serializer.data)
                    else:
                        errors.append({"row": idx + 2, "errors": serializer.errors})

                except Exception as e:
                    errors.append({"row": idx + 2, "error": str(e)})

            return Response({
                "message": f"Processed {len(df)} rows",
                "created": len(created),
                "errors": errors
            }, status=201 if created else 400)

        except Exception as e:
            return Response({"error": f"File processing error: {str(e)}"}, status=500)