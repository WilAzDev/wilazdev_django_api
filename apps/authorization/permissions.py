from django.db.models import Q
from rest_framework import permissions
from apps.authorization.models import Permission

class SafeMethodsForAll(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class HasRoles(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed_roles = getattr(view,'allowed_roles',[])
        user_roles = request.user.roles.values_list("name",flat=True)
        return any(role in allowed_roles for role in user_roles)

class HasPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed_permissions = getattr(view,'allowed_permissions',[])
        user_permissions = set(
            Permission.objects.filter(
                Q(user_has_permissions__user=request.user),
                Q(role_has_permissions__role__user=request.user)
            ).values_list('name',flat=True).distinct()
        )
        return any(permission in allowed_permissions for permission in user_permissions)
        
        