from rest_framework import permissions


class AdminOrReadOnly(permissions.IsAdminUser):

    @staticmethod
    def has_permission(request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            bool(request.user and request.user.is_staff)


class ReviewUserOrReadOnly(permissions.BasePermission):

    @staticmethod
    def has_object_permission(request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.review_user == request.user
