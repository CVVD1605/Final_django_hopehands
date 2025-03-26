# volunteer/permissions.py]
from rest_framework import permissions

class IsAuthenticatedOrCreate(permissions.BasePermission):
    """
    Custom permission to allow access to profile creation without authentication.
    For other actions, authentication is required.
    """
    def has_permission(self, request, view):
        # Allow profile creation without authentication
        if request.method == 'POST':
            return True
        # For other methonds, (GET, PUT, DELETE) require authentication
        return request.user and request.user.is_authenticated
