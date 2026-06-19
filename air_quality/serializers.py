from rest_framework import serializers
from .models import AirQuality

class AirQualitySerializer(serializers.ModelSerializer):
    industry_name = serializers.CharField(source="industry.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    air_quality_category = serializers.ReadOnlyField()

    class Meta:
        model = AirQuality
        fields = [
            "id", "industry", "industry_name", "department", "department_name",
            "date", "aqi", "pm25", "pm10", "co2", "no2", "so2",
            "temperature", "humidity",  # Added
            "air_quality_category", "created_at"
        ]
        read_only_fields = ["id", "created_at", "air_quality_category"]

    def validate_aqi(self, value):
        if value < 0:
            raise serializers.ValidationError("AQI cannot be negative")
        return value