from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    class Meta:
        db_table = 'users'

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