from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ApprovalWorkflow(models.Model):
    STATUS_PENDING = "Pending"
    STATUS_ANALYST_REVIEW = "Analyst Review"
    STATUS_MANAGER_APPROVED = "Manager Approved"
    STATUS_SUPERVISOR_APPROVED = "Supervisor Approved"
    STATUS_REJECTED = "Rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_ANALYST_REVIEW, STATUS_ANALYST_REVIEW),
        (STATUS_MANAGER_APPROVED, STATUS_MANAGER_APPROVED),
        (STATUS_SUPERVISOR_APPROVED, STATUS_SUPERVISOR_APPROVED),
        (STATUS_REJECTED, STATUS_REJECTED),
    ]

    ACTION_SUBMIT = "submit"
    ACTION_APPROVE = "approve"
    ACTION_REJECT = "reject"
    ACTION_ESCALATE = "escalate"

    ACTION_CHOICES = [
        (ACTION_SUBMIT, "Submit"),
        (ACTION_APPROVE, "Approve"),
        (ACTION_REJECT, "Reject"),
        (ACTION_ESCALATE, "Escalate"),
    ]

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    current_status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_workflows",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_workflows",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("content_type", "object_id")
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Workflow {self.id} [{self.current_status}] for {self.content_type.app_label}.{self.object_id}"

    def _log(self, action, user, comment=None):
        WorkflowLog.objects.create(
            workflow=self,
            action=action,
            performed_by=user,
            role=getattr(user, "role", None) if user else None,
            comment=comment or "",
        )

    def submit(self, user, assigned_to=None, comment=None):
        if self.current_status != self.STATUS_PENDING:
            raise ValueError("Only workflows in Pending state may be submitted.")

        if assigned_to:
            self.assigned_to = assigned_to
        self.save()
        self._log(self.ACTION_SUBMIT, user, comment)

    def approve(self, user, comment=None):
        if user.is_analyst and self.current_status == self.STATUS_PENDING:
            self.current_status = self.STATUS_ANALYST_REVIEW
        elif user.is_manager and self.current_status == self.STATUS_ANALYST_REVIEW:
            self.current_status = self.STATUS_MANAGER_APPROVED
        elif user.is_supervisor and self.current_status == self.STATUS_MANAGER_APPROVED:
            self.current_status = self.STATUS_SUPERVISOR_APPROVED
        elif user.is_admin:
            if self.current_status == self.STATUS_PENDING:
                self.current_status = self.STATUS_ANALYST_REVIEW
            elif self.current_status == self.STATUS_ANALYST_REVIEW:
                self.current_status = self.STATUS_MANAGER_APPROVED
            elif self.current_status == self.STATUS_MANAGER_APPROVED:
                self.current_status = self.STATUS_SUPERVISOR_APPROVED
            else:
                raise ValueError("Workflow cannot be approved from its current status")
        else:
            raise ValueError("Workflow cannot be approved from its current status")

        self.save()
        self._log(self.ACTION_APPROVE, user, comment)

    def reject(self, user, comment=None):
        if self.current_status == self.STATUS_REJECTED:
            raise ValueError("Workflow is already rejected.")

        self.current_status = self.STATUS_REJECTED
        self.save()
        self._log(self.ACTION_REJECT, user, comment)

    def escalate(self, user, comment=None):
        if self.current_status == self.STATUS_REJECTED:
            raise ValueError("Cannot escalate a rejected workflow.")

        if self.current_status == self.STATUS_PENDING:
            self.current_status = self.STATUS_ANALYST_REVIEW
        elif self.current_status == self.STATUS_ANALYST_REVIEW:
            self.current_status = self.STATUS_MANAGER_APPROVED
        elif self.current_status == self.STATUS_MANAGER_APPROVED:
            self.current_status = self.STATUS_SUPERVISOR_APPROVED

        self.assigned_to = user
        self.save()
        self._log(self.ACTION_ESCALATE, user, comment)


class WorkflowLog(models.Model):
    workflow = models.ForeignKey(
        ApprovalWorkflow,
        related_name="logs",
        on_delete=models.CASCADE,
    )
    action = models.CharField(max_length=20, choices=ApprovalWorkflow.ACTION_CHOICES)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="workflow_logs",
    )
    role = models.CharField(max_length=50, blank=True)
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.workflow} - {self.action} by {self.performed_by or 'system'}"
