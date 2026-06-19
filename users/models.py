from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('data_entry', 'Data Entry Operator'),
        ('analyst', 'Analyst'),
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
        ('admin', 'Administrator'),
    )

    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='data_entry')
    industry = models.ForeignKey(
        'industries.Industry',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True
    )

    def __str__(self):
        return self.username

    @property
    def is_data_entry(self):
        return self.role == 'data_entry'

    @property
    def is_analyst(self):
        return self.role == 'analyst'

    @property
    def is_manager(self):
        return self.role == 'manager'

    @property
    def is_supervisor(self):
        return self.role == 'supervisor'

    @property
    def is_admin(self):
        return self.role == 'admin'