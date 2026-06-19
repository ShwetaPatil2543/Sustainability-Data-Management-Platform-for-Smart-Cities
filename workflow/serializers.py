from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import ApprovalWorkflow, WorkflowLog

User = get_user_model()


class WorkflowLogSerializer(serializers.ModelSerializer):
    performed_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = WorkflowLog
        fields = ["id", "action", "performed_by", "role", "comment", "timestamp"]


class ApprovalWorkflowSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        slug_field="model",
        queryset=ContentType.objects.all(),
    )
    created_by = serializers.StringRelatedField(read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )
    logs = WorkflowLogSerializer(many=True, read_only=True)

    class Meta:
        model = ApprovalWorkflow
        fields = [
            "id",
            "content_type",
            "object_id",
            "current_status",
            "created_by",
            "assigned_to",
            "created_at",
            "updated_at",
            "logs",
        ]
        read_only_fields = ["current_status", "created_by", "created_at", "updated_at", "logs"]

    def validate(self, data):
        if data.get("content_type") and data.get("object_id") is None:
            raise serializers.ValidationError("object_id is required when content_type is provided.")
        return data
