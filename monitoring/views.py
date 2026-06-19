from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AQIRecord, CarbonEmission
from .serializers import AQIRecordSerializer, CarbonEmissionSerializer


class AQIRecordViewSet(viewsets.ModelViewSet):
    queryset = AQIRecord.objects.all().order_by('-date')
    serializer_class = AQIRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        industry = self.request.query_params.get('industry')
        if industry:
            qs = qs.filter(industry__id=industry)
        return qs

    @action(detail=False, methods=['post'])
    def compute(self, request):
        """Compute AQI for one or more readings.

        Accepts either a single object or a list of objects with keys: pm25, pm10, no2, so2, co, industry (optional), date (optional).
        If `save=true` is passed as query param, results will be saved to `AQIRecord`.
        """
        from .services.aqi import compute_aqi, compute_bulk

        data = request.data
        save = request.query_params.get('save', 'false').lower() == 'true'

        items = data if isinstance(data, list) else [data]
        results = []
        for item in items:
            reading = {
                'pm25': item.get('pm25'),
                'pm10': item.get('pm10'),
                'no2': item.get('no2'),
                'so2': item.get('so2'),
                'co': item.get('co'),
            }
            res = compute_aqi(reading)
            # optionally persist
            if save:
                try:
                    rec = AQIRecord.objects.create(
                        industry_id=item.get('industry'),
                        date=item.get('date'),
                        pm25=item.get('pm25') or 0,
                        pm10=item.get('pm10') or 0,
                        no2=item.get('no2') or 0,
                        so2=item.get('so2') or 0,
                        co=item.get('co') or 0,
                        aqi=res['aqi'],
                        category=res['category'],
                        computed=True,
                    )
                    res['saved_id'] = rec.id
                except Exception as e:
                    res['save_error'] = str(e)
            results.append(res)

        return Response(results)


class CarbonEmissionViewSet(viewsets.ModelViewSet):
    queryset = CarbonEmission.objects.all().order_by('-date')
    serializer_class = CarbonEmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        industry = self.request.query_params.get('industry')
        if industry:
            qs = qs.filter(industry__id=industry)
        return qs

    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        """Accepts a list of emission objects and bulk creates or updates by industry+date."""
        data = request.data
        if not isinstance(data, list):
            return Response({'detail': 'Expected a list of objects.'}, status=status.HTTP_400_BAD_REQUEST)

        created = 0
        errors = []
        for idx, item in enumerate(data):
            serializer = self.get_serializer(data=item)
            if serializer.is_valid():
                obj, created_flag = CarbonEmission.objects.update_or_create(
                    industry_id=serializer.validated_data['industry'],
                    date=serializer.validated_data['date'],
                    defaults=serializer.validated_data,
                )
                if created_flag:
                    created += 1
            else:
                errors.append({'index': idx, 'errors': serializer.errors})

        return Response({'created': created, 'errors': errors}, status=status.HTTP_200_OK)
