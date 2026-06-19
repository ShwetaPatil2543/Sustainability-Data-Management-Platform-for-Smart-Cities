from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden

class RoleRequiredMixin(UserPassesTestMixin):
    """
    Restrict access to users with specific roles.
    Usage:
    class MyView(RoleRequiredMixin, TemplateView):
        allowed_roles = ['Admin', 'Manager']
    """
    allowed_roles = []

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in self.allowed_roles

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this page.")