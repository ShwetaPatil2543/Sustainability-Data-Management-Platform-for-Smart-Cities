from django.db import models
from django.conf import settings
from industries.models import Industry, Department


class CarbonEmission(models.Model):
    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        related_name="carbon_emissions"
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="department_emissions",
        null=True,
        blank=True
    )

    date = models.DateField()

    fuel_type = models.CharField(max_length=100, blank=True, null=True)
    fuel_amount = models.FloatField(blank=True, null=True)
    emission_factor = models.FloatField(blank=True, null=True)

    co2_emission = models.FloatField(default=0)
    methane_emission = models.FloatField(default=0)
    nitrous_oxide = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    # Stored total to speed up aggregations and allow indexing. Nullable
    # to preserve backward compatibility; a computed fallback is available
    # when this field is null.
    total_emission = models.FloatField(null=True, blank=True)

    # Source of the record: manual entry, bulk upload, sensor import, or predicted
    SOURCE_CHOICES = [
        ("manual", "manual"),
        ("bulk", "bulk"),
        ("sensor", "sensor"),
        ("predicted", "predicted"),
    ]
    source = models.CharField(max_length=32, choices=SOURCE_CHOICES, default="manual")

    # Validation state for the record
    VALIDATION_CHOICES = [
        ("valid", "valid"),
        ("pending", "pending"),
        ("invalid", "invalid"),
    ]
    validation_status = models.CharField(max_length=32, choices=VALIDATION_CHOICES, default="valid")

    @property
    def computed_total_emission(self):
        return (
            (self.co2_emission or 0) +
            (self.methane_emission or 0) +
            (self.nitrous_oxide or 0)
        )

    def save(self, *args, **kwargs):
        # Auto-calculate CO2 if fuel data is provided
        if self.fuel_amount and self.emission_factor:
            self.co2_emission = self.fuel_amount * self.emission_factor
        # Ensure stored total_emission is populated if not provided
        if self.total_emission is None:
            self.total_emission = (
                (self.co2_emission or 0) +
                (self.methane_emission or 0) +
                (self.nitrous_oxide or 0)
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.industry.name} | {self.date}"

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['industry', 'date', 'fuel_type'],
                name='unique_industry_fuel_emission'
            )
        ]
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['industry', 'date']),
        ]


class UploadAudit(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('failed', 'failed'),
    ]

    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    filename = models.CharField(max_length=512, blank=True, null=True)
    idempotency_key = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    file_hash = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    created_count = models.IntegerField(default=0)
    updated_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    skipped_count = models.IntegerField(default=0)
    processing_status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"UploadAudit {self.id} - {self.filename} - {self.processing_status}"