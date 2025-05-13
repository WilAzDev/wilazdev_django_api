from django.db import models
from apps.authorization.classes import HasPermissions

# Create your models here.
class Permission(models.Model):
    name = models.CharField(max_length=60,unique=True)
    description = models.CharField(max_length=100,null=True)
    class Meta:
        db_table = 'permissions'


class Role(models.Model,HasPermissions):
    name = models.CharField(max_length=30,unique=True)
    description = models.CharField(max_length=100,null=True)
    permissions = models.ManyToManyField(Permission,related_name='role_has_permissions',through='authorization.RolePermission')
    class Meta:
        db_table='roles'        

class UserRole(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    class Meta:
        db_table='user_roles'
        unique_together = [('user', 'role')]
        
class RolePermission(models.Model):
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    class Meta:
        db_table='role_permissions'
        unique_together = [('permission', 'role')]

class UserPermission(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    class Meta:
        db_table='user_permissions'
        unique_together = [('user', 'permission')]