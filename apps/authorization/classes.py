class HasRoles:
    def assign_roles(self,roles):

        current_roles = set(self.roles.values_list('id',flat=True))
        new_roles = set(roles)
        to_add = new_roles - current_roles
        to_remove = current_roles - new_roles
        self.roles.through.objects.filter(user=self,role_id__in=to_remove).delete()
        
        for role_id in to_add:
            self.roles.through.objects.create(user=self,role_id=role_id)

class HasPermissions:
    def assign_permissions(self,permissions):
        current_permissions = set(self.permissions.values_list('id',flat=True))
        new_permissions = set(permissions)
        to_add = new_permissions - current_permissions
        to_remove = current_permissions - new_permissions
        self.permissions.through.objects.filter(user=self,permission_id__in=to_remove).delete()
        for permission_id in to_add:
            self.permissions.through.objects.create(user=self,permission_id=permission_id)
