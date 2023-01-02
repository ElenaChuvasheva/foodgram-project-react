from rest_framework import permissions


class NotBanned(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous or not request.user.is_banned
