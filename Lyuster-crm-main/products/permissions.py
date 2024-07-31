from rest_framework import permissions

class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superusers to edit or delete an object.
    All users can view and create objects.
    """

    def has_permission(self, request, view):
        # Allow read-only methods for all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow create method for authenticated users
        if request.method == 'POST':
            return request.user and request.user.is_authenticated

        # Allow update and delete methods only for superusers
        return request.user and request.user.is_superuser
