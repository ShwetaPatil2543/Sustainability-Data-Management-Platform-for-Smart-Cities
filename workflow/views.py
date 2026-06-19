from django.contrib.contenttypes.models import ContentType
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ApprovalWorkflow
from .permissions import WorkflowPermission
from .serializers import ApprovalWorkflowSerializer


class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = ApprovalWorkflow.objects.all().select_related("content_type", "created_by", "assigned_to")
    serializer_class = ApprovalWorkflowSerializer
    permission_classes = [IsAuthenticated, WorkflowPermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_admin:
            return qs
        if user.is_analyst:
            return qs.filter(current_status=ApprovalWorkflow.STATUS_PENDING)
        if user.is_manager:
            return qs.filter(current_status=ApprovalWorkflow.STATUS_ANALYST_REVIEW)
        if user.is_supervisor:
            return qs.filter(current_status=ApprovalWorkflow.STATUS_MANAGER_APPROVED)
        if user.is_data_entry:
            return qs.filter(created_by=user)
        return qs.none()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return Response({"detail": "Direct workflow updates are not permitted."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({"detail": "Direct workflow updates are not permitted."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Workflow deletion is not permitted."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        workflow = self.get_object()
        assigned_to = None
        assigned_to_id = request.data.get("assigned_to")
        if assigned_to_id:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                assigned_to = User.objects.get(pk=assigned_to_id)
            except User.DoesNotExist:
                return Response({"detail": "Assigned user not found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            workflow.submit(request.user, assigned_to=assigned_to, comment=request.data.get("comment"))
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_serializer(workflow).data)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        workflow = self.get_object()
        try:
            workflow.approve(request.user, comment=request.data.get("comment"))
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_serializer(workflow).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        workflow = self.get_object()
        try:
            workflow.reject(request.user, comment=request.data.get("comment"))
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_serializer(workflow).data)

    @action(detail=True, methods=["post"])
    def escalate(self, request, pk=None):
        workflow = self.get_object()
        try:
            workflow.escalate(request.user, comment=request.data.get("comment"))
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_serializer(workflow).data)

    @action(detail=False, methods=["get"])
    def queue(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def create_for_record(self, request):
        content_type_model = request.data.get("content_type")
        object_id = request.data.get("object_id")
        if not content_type_model or object_id is None:
            return Response({"detail": "content_type and object_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content_type = ContentType.objects.get(model=content_type_model)
        except ContentType.DoesNotExist:
            return Response({"detail": "Unknown content_type."}, status=status.HTTP_400_BAD_REQUEST)

        workflow, created = ApprovalWorkflow.objects.get_or_create(
            content_type=content_type,
            object_id=object_id,
            defaults={"created_by": request.user},
        )
        serializer = self.get_serializer(workflow)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)
