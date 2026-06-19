from django.db import models


class SustainabilityReport(models.Model):

    industry = models.CharField(max_length=100)

    department = models.CharField(max_length=100)

    date = models.DateField()

    total_emission = models.FloatField()

    def __str__(self):
        return f"{self.industry} - {self.date}"