from rest_framework import serializers
from .models import SustainabilityReport


class SustainabilityReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = SustainabilityReport
        fields = '__all__'