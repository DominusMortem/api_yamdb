from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user and
                    request.user.is_authenticated and
                    request.user.role == 'admin' or
                    request.user.is_staff)


class IsModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.role == 'moderators')


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
