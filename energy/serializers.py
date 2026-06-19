from rest_framework import serializers
from .models import EnergyUsage

class EnergyUsageSerializer(serializers.ModelSerializer):
    industry_name = serializers.CharField(source="industry.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = EnergyUsage
        fields = '__all__'