import copy

from django.contrib.auth.models import Permission
from rest_framework import permissions


class CustomDjangoModelPermission(permissions.DjangoModelPermissions):

    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

    def has_permission(self, request, view):
        permissions = Permission.objects.filter(user=request.user)
        for perm in permissions:
            print(perm)
        print(bool(request.user.has_perm("polls.view_team")))
        return bool(request.user.has_perm("polls.view_team"))

