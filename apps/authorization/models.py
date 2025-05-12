from django.db import models

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=30,unique=True)
    class Meta:
        db_table='roles'        

class UserHasRole(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    class Meta:
        db_table='user_has_roles'
        unique_together = [('user', 'role')]