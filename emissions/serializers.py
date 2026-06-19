from rest_framework import serializers
from .models import CarbonEmission
from datetime import date


class CarbonEmissionSerializer(serializers.ModelSerializer):
    industry_name = serializers.CharField(source="industry.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    # Provide stored total_emission when present, otherwise compute from components
    total_emission = serializers.SerializerMethodField(read_only=True)
    nitrous_emission = serializers.FloatField(source="nitrous_oxide", required=False)

    class Meta:
        model = CarbonEmission
        fields = [
            "id", "industry", "industry_name", "department", "department_name",
            "date", "fuel_type", "fuel_amount", "emission_factor", "co2_emission",
            "methane_emission", "nitrous_emission", "total_emission", "created_at",
            "source", "validation_status",
        ]
        read_only_fields = ["id", "created_at", "total_emission"]

    def get_total_emission(self, obj):
        if obj.total_emission is not None:
            return obj.total_emission
        return obj.computed_total_emission

    def validate_co2_emission(self, value):
        if value < 0:
            raise serializers.ValidationError("CO2 emission cannot be negative")
        return value

    def validate_methane_emission(self, value):
        if value < 0:
            raise serializers.ValidationError("Methane emission cannot be negative")
        return value

    # Validator for mapped nitrous_emission field (source nitrous_oxide)
    def validate_nitrous_emission(self, value):
        if value is None:
            return value
        if value < 0:
            raise serializers.ValidationError("Nitrous emission cannot be negative")
        return value

    def validate_date(self, value):
        # Reject future dates by default; allow predicted records by explicit source
        if value > date.today():
            src = self.initial_data.get('source')
            if src != 'predicted':
                raise serializers.ValidationError("Date cannot be in the future")
        return value


class TotalsSerializer(serializers.Serializer):
    total = serializers.FloatField()
    average = serializers.FloatField()


class IndustryBreakdownSerializer(serializers.Serializer):
    industry = serializers.CharField()
    industry_id = serializers.IntegerField()
    total = serializers.FloatField()


class DepartmentBreakdownSerializer(serializers.Serializer):
    department = serializers.CharField()
    department_id = serializers.IntegerField(allow_null=True)
    total = serializers.FloatField()


class TrendPointSerializer(serializers.Serializer):
    period = serializers.CharField()
    total = serializers.FloatField()


class TopEmitterSerializer(serializers.Serializer):
    industry = serializers.CharField()
    industry_id = serializers.IntegerField()
    total = serializers.FloatField()


class DashboardSummarySerializer(serializers.Serializer):
    total_emissions = serializers.FloatField()
    average_emissions = serializers.FloatField()
    growth_pct = serializers.FloatField()
    top_emitters = TopEmitterSerializer(many=True)
    sustainability_score = serializers.FloatField()


class UploadAuditSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    filename = serializers.CharField(allow_null=True)
    idempotency_key = serializers.CharField(allow_null=True)
    file_hash = serializers.CharField(allow_null=True)
    created_count = serializers.IntegerField()
    updated_count = serializers.IntegerField()
    failed_count = serializers.IntegerField()
    skipped_count = serializers.IntegerField()
    processing_status = serializers.CharField()
    started_at = serializers.DateTimeField(allow_null=True)
    finished_at = serializers.DateTimeField(allow_null=True)
    error_message = serializers.CharField(allow_null=True)