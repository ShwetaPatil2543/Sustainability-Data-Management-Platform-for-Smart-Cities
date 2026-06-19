from rest_framework.permissions import BasePermission

class AirQualityPermission(BasePermission):
    """
    Custom permission for air quality data based on user roles.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        user_role = request.user.role

        # Admin has full access
        if user_role == 'admin':
            return True

        # Manager can read/write their industry data
        if user_role == 'manager':
            return request.method in ['GET', 'POST', 'PUT', 'PATCH']

        # Analyst can only read data
        if user_role == 'analyst':
            return request.method in ['GET']

        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        user_role = request.user.role

        # Admin has full access
        if user_role == 'admin':
            return True

        # Check if the object belongs to user's industry
        if hasattr(obj, 'industry') and obj.industry:
            if request.user.industry != obj.industry:
                return False

        # Manager can modify their industry data
        if user_role == 'manager':
            return True

        # Analyst can only read
        if user_role == 'analyst':
            return request.method in ['GET']

        return False