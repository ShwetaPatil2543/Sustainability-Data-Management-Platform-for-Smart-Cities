from django.db import models


class AirQuality(models.Model):
    industry = models.ForeignKey(
        'industries.Industry',
        on_delete=models.CASCADE,
        related_name='air_quality_data',
        null=True,
        blank=True
    )
    department = models.ForeignKey(
        'industries.Department',
        on_delete=models.CASCADE,
        related_name='department_air_quality',
        null=True,
        blank=True
    )
    date = models.DateField()
    aqi = models.IntegerField(help_text="Air Quality Index")
    pm25 = models.FloatField(help_text="PM2.5 concentration in µg/m³")
    pm10 = models.FloatField(help_text="PM10 concentration in µg/m³")
    co2 = models.FloatField(help_text="CO2 concentration in ppm")
    no2 = models.FloatField(help_text="NO2 concentration in µg/m³")
    so2 = models.FloatField(help_text="SO2 concentration in µg/m³")

    # New fields
    temperature = models.FloatField(help_text="Temperature in °C", null=True, blank=True)
    humidity = models.FloatField(help_text="Humidity in %", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def air_quality_category(self):
        if self.aqi <= 50:
            return "Good"
        elif self.aqi <= 100:
            return "Moderate"
        elif self.aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif self.aqi <= 200:
            return "Unhealthy"
        elif self.aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"

    def __str__(self):
        return f"{self.industry or 'Global'} - AQI: {self.aqi} ({self.air_quality_category})"

    class Meta:
        ordering = ['-date']
        verbose_name = "Air Quality Data"
        verbose_name_plural = "Air Quality Data"