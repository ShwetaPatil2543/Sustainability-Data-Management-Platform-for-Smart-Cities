from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    class Meta:
        abstract = True


class AQIRecord(TimeStampedModel):
    industry = models.ForeignKey('industries.Industry', on_delete=models.CASCADE)
    date = models.DateField()
    pm25 = models.FloatField(default=0)
    pm10 = models.FloatField(default=0)
    no2 = models.FloatField(default=0)
    so2 = models.FloatField(default=0)
    co = models.FloatField(default=0)
    aqi = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=50, blank=True)
    computed = models.BooleanField(default=False)

    class Meta:
        unique_together = (('industry', 'date'),)
        indexes = [models.Index(fields=['industry', 'date'])]

    def __str__(self):
        return f"AQI {self.industry} - {self.date} : {self.aqi}"


class CarbonEmission(TimeStampedModel):
    industry = models.ForeignKey('industries.Industry', on_delete=models.CASCADE)
    date = models.DateField()
    co2_emission = models.FloatField(default=0)
    methane_emission = models.FloatField(default=0)
    nitrous_emission = models.FloatField(default=0)
    total_emission = models.FloatField(null=True, blank=True)
    source = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = (('industry', 'date'),)
        indexes = [models.Index(fields=['industry', 'date'])]

    def save(self, *args, **kwargs):
        self.total_emission = (
            (self.co2_emission or 0) + (self.methane_emission or 0) + (self.nitrous_emission or 0)
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Emissions {self.industry} - {self.date} : {self.total_emission}"


class EmissionFactor(models.Model):
    """Admin-manageable emission factors to override defaults.

    Example fuel_type: 'diesel', 'coal', 'electricity'
    """
    fuel_type = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=50, default='unit')
    co2_kg_per_unit = models.FloatField(default=0)
    ch4_kg_per_unit = models.FloatField(default=0)
    n2o_kg_per_unit = models.FloatField(default=0)

    class Meta:
        verbose_name = 'Emission Factor'
        verbose_name_plural = 'Emission Factors'

    def __str__(self):
        return f"{self.fuel_type} ({self.unit})"
