from django.contrib import admin
from .models import Industry, Department


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "industry_type", "location", "created_at")

    search_fields = ("name", "location")

    list_filter = ("industry_type",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "industry", "manager_name")

    search_fields = ("name", "manager_name")

    list_filter = ("industry",)