from django.db import models

class EnergyUsage(models.Model):
    industry = models.ForeignKey(
        "industries.Industry",
        on_delete=models.CASCADE,
        related_name="energy_usage",
        null=True, blank=True
    )
    department = models.ForeignKey(
        "industries.Department",
        on_delete=models.CASCADE,
        related_name="department_energy",
        null=True, blank=True
    )
    date = models.DateField()
    electricity_consumption = models.FloatField(help_text="Electricity consumption in kWh")
    renewable_energy = models.FloatField(help_text="Renewable energy used in kWh")
    non_renewable_energy = models.FloatField(help_text="Non-renewable energy used in kWh")
    total_energy = models.FloatField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_energy = self.electricity_consumption  # auto-calc total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.industry or self.department} - {self.total_energy} kWh"