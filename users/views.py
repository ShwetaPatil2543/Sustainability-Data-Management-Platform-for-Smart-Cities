from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CurrentUserSerializer


class CurrentUserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Allow the current user to update their profile (partial updates allowed)."""
        serializer = CurrentUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request):
        return self.put(request)

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import CurrentUserSerializer


class LogoutView(APIView):
    """Blacklist a refresh token to log out a user.

    POST { "refresh": "<token>" }
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'detail': 'Refresh token required.'}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Admin-only user listing and retrieval."""

    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Only admin role allowed to list users
        user = self.request.user
        if user.is_authenticated and user.is_admin:
            return [perm() for perm in self.permission_classes]
        from rest_framework.permissions import IsAdminUser
        return [IsAdminUser()]