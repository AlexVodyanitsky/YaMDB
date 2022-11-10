from enum import Enum

from rest_framework.permissions import BasePermission, SAFE_METHODS


class Roles(Enum):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            is_superuser = request.user.is_superuser
            is_admin = request.user.role == Roles.ADMIN.value
            return is_admin or is_superuser
        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        is_superuser = request.user.is_superuser
        is_admin = (
            request.user.is_authenticated
            and request.user.role == Roles.ADMIN.value
        )
        return is_admin or is_superuser


class ReviewCommentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'DELETE'):
            is_admin = request.user.role == Roles.ADMIN.value
            is_superuser = request.user.is_superuser
            is_moderator = request.user.role == Roles.MODERATOR.value
            is_author = obj.author == request.user
            return is_admin or is_superuser or is_moderator or is_author
        return True
