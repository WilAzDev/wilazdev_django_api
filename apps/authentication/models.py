from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.authorization.models import Role

class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    roles = models.ManyToManyField(Role,related_name='user_has_roles',through='authorization.UserRole')
    
    class Meta:
        db_table = 'users'
    
    def assign_roles(self,roles):

        current_roles = set(self.roles.values_list('id',flat=True))
        new_roles = set(roles)
        to_add = new_roles - current_roles
        to_remove = current_roles - new_roles
        self.roles.through.objects.filter(user=self,role_id__in=to_remove).delete()
        
        for role_id in to_add:
            self.roles.through.objects.create(user=self,role_id=role_id)

class Gender(models.Model):
    name = models.CharField(max_length=100)
    short = models.CharField(max_length=7)
    
    class Meta:
        db_table = 'genders'

class Profile(models.Model):
    first_name = models.CharField(max_length=150)
    second_name = models.CharField(max_length=150,null=True)
    last_name = models.CharField(max_length=150)
    second_last_name = models.CharField(max_length=150,null=True)
    gender = models.ForeignKey(Gender,null=True ,on_delete=models.SET_NULL)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'profiles'