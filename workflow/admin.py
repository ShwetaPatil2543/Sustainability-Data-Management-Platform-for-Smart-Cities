from django.contrib import admin

from .models import ApprovalWorkflow, WorkflowLog


@admin.register(ApprovalWorkflow)
class ApprovalWorkflowAdmin(admin.ModelAdmin):
    list_display = ("id", "content_type", "object_id", "current_status", "created_by", "assigned_to", "updated_at")
    list_filter = ("current_status", "content_type", "created_by", "assigned_to")
    search_fields = ("content_type__model", "object_id", "created_by__username", "assigned_to__username")


@admin.register(WorkflowLog)
class WorkflowLogAdmin(admin.ModelAdmin):
    list_display = ("workflow", "action", "performed_by", "role", "timestamp")
    list_filter = ("action", "role", "timestamp")
    search_fields = ("performed_by__username", "comment")
