from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
import pandas as pd
from datetime import datetime, timedelta
from .models import AirQuality
from industries.models import Industry, Department


class AirQualityViewSet(viewsets.ModelViewSet):
    queryset = AirQuality.objects.all().order_by('-date')
    serializer_class = None  # Add your serializer if needed
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='upload')
    def upload_file(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read Excel or CSV
            if file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            elif file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                return Response({"error": "Unsupported file type"}, status=400)

            df.columns = df.columns.str.strip()  # remove spaces
            column_mapping = {
                'date': ['date', 'Date', 'DATE'],
                'aqi': ['aqi', 'AQI'],
                'pm25': ['pm25', 'PM2.5'],
                'pm10': ['pm10', 'PM10'],
                'co2': ['co2', 'CO2'],
                'no2': ['no2', 'NO2'],
                'so2': ['so2', 'SO2'],
                'temperature': ['temperature', 'temp'],
                'humidity': ['humidity', 'Humidity'],
                'industry': ['industry', 'Industry'],
                'department': ['department', 'Department']
            }

            # Map columns
            mapped_df = pd.DataFrame()
            for key, aliases in column_mapping.items():
                for alias in aliases:
                    if alias in df.columns:
                        mapped_df[key] = df[alias]
                        break

            created_count = 0
            updated_count = 0
            errors = []

            for idx, row in mapped_df.iterrows():
                try:
                    row_dict = row.to_dict()

                    # --- FIX: Convert Excel serial date to datetime ---
                    date_val = row_dict.get('date')
                    if pd.isna(date_val):
                        raise ValueError("Missing date")
                    if isinstance(date_val, (float, int)):
                        date_val = datetime(1899, 12, 30) + timedelta(days=date_val)
                    elif isinstance(date_val, str):
                        date_val = pd.to_datetime(date_val)

                    # --- Industry / Department ---
                    industry = None
                    department = None
                    if 'industry' in row_dict and pd.notna(row_dict['industry']):
                        industry, _ = Industry.objects.get_or_create(name=str(row_dict['industry']))
                    if 'department' in row_dict and pd.notna(row_dict['department']) and industry:
                        department, _ = Department.objects.get_or_create(
                            name=str(row_dict['department']),
                            defaults={'industry': industry}
                        )

                    # --- Prepare defaults ---
                    defaults = {
                        'aqi': row_dict.get('aqi') or 0,
                        'pm25': row_dict.get('pm25') or 0,
                        'pm10': row_dict.get('pm10') or 0,
                        'co2': row_dict.get('co2'),
                        'no2': row_dict.get('no2'),
                        'so2': row_dict.get('so2'),
                        'temperature': row_dict.get('temperature'),
                        'humidity': row_dict.get('humidity'),
                        'industry': industry,
                        'department': department
                    }
                    # Remove None
                    defaults = {k: v for k, v in defaults.items() if v is not None}

                    # --- Save row ---
                    obj, created = AirQuality.objects.update_or_create(date=date_val, defaults=defaults)
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                except Exception as e:
                    errors.append(f"Row {idx + 1}: {str(e)}")

            result = {
                "message": f"Processed {len(mapped_df)} rows",
                "created": created_count,
                "updated": updated_count,
            }
            if errors:
                result["errors"] = errors[:20]

            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"File processing failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)