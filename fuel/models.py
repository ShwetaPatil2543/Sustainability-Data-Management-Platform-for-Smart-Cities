from django.db import models

# Create your models here.
from django.db import models


class FuelConsumption(models.Model):

    industry = models.ForeignKey(
        "industries.Industry",
        on_delete=models.CASCADE,
        related_name="fuel_usage"
    )

    department = models.ForeignKey(
        "industries.Department",
        on_delete=models.CASCADE,
        related_name="department_fuel"
    )

    date = models.DateField()

    fuel_type = models.CharField(
        max_length=100,
        help_text="Diesel, Petrol, Natural Gas, Coal, etc"
    )

    quantity = models.FloatField(
        help_text="Fuel quantity in liters or kg"
    )

    cost = models.FloatField()

    carbon_emission_factor = models.FloatField(
        help_text="Emission factor for this fuel"
    )

    total_emission = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.industry.name} - {self.fuel_type}"