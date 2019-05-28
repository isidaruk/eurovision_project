from rest_framework import permissions


class VotingPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        pass
