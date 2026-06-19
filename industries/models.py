from django.db import models


class Industry(models.Model):

    INDUSTRY_TYPES = [
        ("manufacturing", "Manufacturing"),
        ("chemical", "Chemical"),
        ("energy", "Energy"),
        ("construction", "Construction"),
        ("textile", "Textile"),
        ("pharmaceutical", "Pharmaceutical"),
    ]

    name = models.CharField(max_length=255)

    industry_type = models.CharField(
        max_length=50,
        choices=INDUSTRY_TYPES,
        default="manufacturing"
    )

    location = models.CharField(max_length=255)

    contact_email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Department(models.Model):

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        related_name="departments"
    )

    name = models.CharField(max_length=200)

    manager_name = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.industry.name}"