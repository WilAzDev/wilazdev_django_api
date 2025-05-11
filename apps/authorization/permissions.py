from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        allow_safe_methods = getattr(view,'allow_safe_methods',True)
        if not allow_safe_methods:
            return False
        return request.method in permissions.SAFE_METHODS

class HasRoles(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        allowed_roles = getattr(view,'allowed_roles',None)
        allow_safe_methods = getattr(view,'allow_safe_methods',True)
       
        if not allowed_roles and not allow_safe_methods:
            return False
        elif not allowed_roles and allow_safe_methods:
            return request.method in permissions.SAFE_METHODS
        
        user_roles = request.user.roles.values_list('name',flat=True)
        return any(role in allowed_roles for role in user_roles)
        