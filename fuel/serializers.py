from rest_framework import serializers
from .models import FuelConsumption


class FuelConsumptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FuelConsumption
        fields = '__all__'