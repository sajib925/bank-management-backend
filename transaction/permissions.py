from rest_framework.permissions import BasePermission

class IsNormalUser(BasePermission):
    """
    Allows access only to normal users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'normalusers')

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'adminusers')
