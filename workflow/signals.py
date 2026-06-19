from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ApprovalWorkflow

TARGET_MODELS = [
    ("air_quality", "airquality"),
    ("emissions", "carbonemission"),
    ("energy", "energyusage"),
    ("fuel", "fuelconsumption"),
]


def _is_workflow_model(sender):
    return (sender._meta.app_label, sender._meta.model_name) in TARGET_MODELS


@receiver(post_save)
def create_workflow_for_record(sender, instance, created, **kwargs):
    if not created or not _is_workflow_model(sender):
        return

    content_type = ContentType.objects.get_for_model(sender)
    ApprovalWorkflow.objects.get_or_create(
        content_type=content_type,
        object_id=instance.pk,
        defaults={
            "created_by": getattr(instance, "created_by", None),
            "current_status": ApprovalWorkflow.STATUS_PENDING,
        },
    )
