from __future__ import annotations
from datetime import datetime
from .models import UploadAudit
from .utils import parse_payload, normalize_row
from .views import _process_rows_sync
import io

try:
    from celery import shared_task
    CELERY_AVAILABLE = True
except Exception:
    CELERY_AVAILABLE = False


if CELERY_AVAILABLE:
    @shared_task(bind=True)
    def process_bulk_upload(self, audit_id: int, file_bytes: bytes, filename: str, json_payload=None, options=None):
        audit = UploadAudit.objects.get(id=audit_id)
        audit.processing_status = 'processing'
        audit.started_at = datetime.utcnow()
        audit.save()
        try:
            rows, file_hash = parse_payload(io.BytesIO(file_bytes), filename, json_payload=json_payload)
            # delegate to sync helper
            result = _process_rows_sync(rows, audit=audit, dry_run=(options or {}).get('dry_run', False))
            audit.created_count = result.get('created', 0)
            audit.failed_count = len(result.get('errors', []))
            audit.processing_status = 'completed'
            audit.finished_at = datetime.utcnow()
            audit.save()
            return result
        except Exception as e:
            audit.processing_status = 'failed'
            audit.error_message = str(e)
            audit.finished_at = datetime.utcnow()
            audit.save()
            raise
