from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Industry, Department
from .serializers import IndustrySerializer, DepartmentSerializer


class IndustryViewSet(viewsets.ModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]