from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    """
    Allow access only to users with certain roles.
    """
    allowed_roles = []

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in self.allowed_roles


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_manager)


class IsAnalyst(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_analyst)


class IsDataEntry(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_data_entry)


class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_supervisor)


class AllowRoles(BasePermission):
    """Usage: set view.allowed_roles = ['admin','manager']"""
    def has_permission(self, request, view):
        allowed = getattr(view, 'allowed_roles', None)
        if allowed is None:
            return False
        return bool(request.user and request.user.is_authenticated and request.user.role in allowed)