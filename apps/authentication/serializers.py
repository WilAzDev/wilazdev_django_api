from typing import Dict,Any,List
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .types import UserValidationData
from rest_framework import serializers
from .models import User
import re

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )
    class Meta:
        model = User
        fields = ('username','email','password','password2','is_active')
    
    def validate(self, attrs:Dict[str,Any])->UserValidationData:
        errors:Dict[str,List[str]] = {}
        
        attrs['username'] = attrs.get('username').strip()
        attrs['email'] = attrs.get('email').strip()
        attrs['password'] = attrs.get('password').strip()
        attrs['password2'] = attrs.get('password2').strip()
        attrs['is_active'] = False
        
        username:str = attrs['username']
        if not re.match(r'^[A-Za-z][A-Za-z0-9]*$',username):
            errors.setdefault('username', []).append('El username solo debe contener letras y numeros')
        if not re.match(r'^.{3,20}$',username):
            errors.setdefault('username',[]).append('El username debe tener entre 3 y 20 caracteres')
        if ' ' in username:
            errors.setdefault('username',[]).append('El username no puede contener espacios')
        if User.objects.filter(username=username).first():
            errors.setdefault('username',[]).append('El username ya existe')
            
        email:str = attrs['email']
        try:
            validate_email(email)
        except ValidationError:
            errors.setdefault('email',[]).append('El email no es valido')
        if len(email) > 254:
            errors.setdefault('email',[]).append('El email no puede tener mas de 254 caracteres')
        if User.objects.filter(email=email).first():
            errors.setdefault('email',[]).append('El email ya esta en uso')
        
        password:str = attrs['password']
        password2:str = attrs['password2']
        if password != password2:
            errors.setdefault('password',[]).append('Las contraseñas no coinciden')
        if len(password) < 16 or len(password) > 128:
            errors.setdefault('password',[]).append('La contraseña debe tener entre 16 y 128')
        if not re.search(r'[A-Z]',password):
            errors.setdefault('password',[]).append('La contraseña debe tener al menos una mayuscula')
        if not re.search(r'\d',password):
            errors.setdefault('password',[]).append('La contraseña debe tener al menos un digito')
        if not re.search(r"[!@#$%^&*()_=+|;:,<.>/?-]", password):
            errors.setdefault('password',[]).append('La contraseña debe tener al menos un caracter especial')
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs

    def create(self, validated_data:UserValidationData)->User:
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)
