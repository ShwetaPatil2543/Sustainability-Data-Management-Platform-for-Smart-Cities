from rest_framework.permissions import BasePermission


class WorkflowPermission(BasePermission):
    """Strict role-based access for workflow queue and actions."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        action = getattr(view, "action", None)

        if action in ["list", "retrieve", "queue", "create", "create_for_record"]:
            return True

        if action == "submit":
            return request.user.is_data_entry or request.user.is_admin

        if action == "approve":
            return request.user.is_analyst or request.user.is_manager or request.user.is_supervisor or request.user.is_admin

        if action == "reject":
            return request.user.is_analyst or request.user.is_manager or request.user.is_supervisor or request.user.is_admin

        if action == "escalate":
            return request.user.is_manager or request.user.is_supervisor or request.user.is_admin

        return False

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_admin:
            return True

        action = getattr(view, "action", None)

        if action in ["retrieve", "list", "queue"]:
            return self._can_view(request, obj)

        if action == "submit":
            return self._can_submit(request, obj)

        if action == "approve":
            return self._can_approve(request, obj)

        if action == "reject":
            return self._can_reject(request, obj)

        if action == "escalate":
            return self._can_escalate(request, obj)

        return False

    def _can_view(self, request, obj):
        if request.user.is_data_entry:
            return obj.created_by_id == request.user.id
        if request.user.is_analyst:
            return obj.current_status == obj.STATUS_PENDING
        if request.user.is_manager:
            return obj.current_status == obj.STATUS_ANALYST_REVIEW
        if request.user.is_supervisor:
            return obj.current_status == obj.STATUS_MANAGER_APPROVED
        return False

    def _can_submit(self, request, obj):
        return obj.current_status == obj.STATUS_PENDING and (request.user.is_data_entry or request.user.is_admin)

    def _can_approve(self, request, obj):
        return (
            (request.user.is_analyst and obj.current_status == obj.STATUS_PENDING)
            or (request.user.is_manager and obj.current_status == obj.STATUS_ANALYST_REVIEW)
            or (request.user.is_supervisor and obj.current_status == obj.STATUS_MANAGER_APPROVED)
        )

    def _can_reject(self, request, obj):
        return obj.current_status != obj.STATUS_REJECTED

    def _can_escalate(self, request, obj):
        return obj.current_status != obj.STATUS_REJECTED
