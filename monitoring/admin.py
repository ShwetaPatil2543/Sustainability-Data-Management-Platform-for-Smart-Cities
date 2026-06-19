from django.contrib import admin
from .models import AQIRecord, CarbonEmission

from .models import EmissionFactor


@admin.register(AQIRecord)
class AQIRecordAdmin(admin.ModelAdmin):
    list_display = ('industry', 'date', 'aqi', 'category', 'computed')
    list_filter = ('industry', 'computed')
    search_fields = ('industry__name',)


@admin.register(CarbonEmission)
class CarbonEmissionAdmin(admin.ModelAdmin):
    list_display = ('industry', 'date', 'total_emission')
    list_filter = ('industry',)
    search_fields = ('industry__name',)


@admin.register(EmissionFactor)
class EmissionFactorAdmin(admin.ModelAdmin):
    list_display = ('fuel_type', 'unit', 'co2_kg_per_unit', 'ch4_kg_per_unit', 'n2o_kg_per_unit')
    search_fields = ('fuel_type',)
