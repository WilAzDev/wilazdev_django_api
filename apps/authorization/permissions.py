from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        allow_safe_methods = getattr(view,'allow_safe_methods',True)
        if not allow_safe_methods:
            return False
        return request.method in permissions.SAFE_METHODS

class HasRoles(IsSuperAdmin):
    def has_permission(self, request, view):
        allowed_roles = getattr(view,'allowed_roles',None)
       
        if not allowed_roles:
            return True

        user_roles = request.user.roles.values_list('name',flat=True)
        if any(role in allowed_roles for role in user_roles):
            return True
        
        return super().has_permission(self,request,view)
        