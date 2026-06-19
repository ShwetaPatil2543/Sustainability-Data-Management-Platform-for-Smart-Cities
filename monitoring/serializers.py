from rest_framework import serializers
from .models import AQIRecord, CarbonEmission


class AQIRecordSerializer(serializers.ModelSerializer):
    industry_name = serializers.CharField(source='industry.name', read_only=True)

    class Meta:
        model = AQIRecord
        fields = ['id', 'industry', 'industry_name', 'date', 'pm25', 'pm10', 'no2', 'so2', 'co', 'aqi', 'category', 'computed']


class CarbonEmissionSerializer(serializers.ModelSerializer):
    industry_name = serializers.CharField(source='industry.name', read_only=True)

    class Meta:
        model = CarbonEmission
        fields = ['id', 'industry', 'industry_name', 'date', 'co2_emission', 'methane_emission', 'nitrous_emission', 'total_emission', 'source']
