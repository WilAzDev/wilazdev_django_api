from typing import Dict,Any,List
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers,status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken,AuthenticationFailed
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer,
    TokenObtainPairSerializer
)
from ..models import User
import re


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, min_length=3)
    password = serializers.CharField(
        write_only=True,
        max_length=128,
        min_length=16,
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )
    class Meta:
        model = User
        fields = ('username','email','password','password2')
        
    def validate_username(self,value:str):
        value = value.strip()
        username:str = value
        if not re.match(r'^[A-Za-z][A-Za-z0-9]*$',username):
            raise serializers.ValidationError('Username must be alphanumeric')
        if ' ' in username:
            raise serializers.ValidationError('Username must not contain any spaces')
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username is already taken')
        return value
    
    def validate_email(self,value:str):

        value = value.strip()
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError('Invalid email')
        if len(value) > 254:
            raise serializers.ValidationError('Email is too long')
        if User.objects.filter(email=value).first():
            raise serializers.ValidationError('Email is already taken')
        return value
    
    def validate_password(self,value:str):
        value = value.strip()
        
        if not re.search(r'[A-Z]',value):
            raise serializers.ValidationError('Password must contain at least one capital letter')
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:'\",.<>/?`~\\]",value):
            raise serializers.ValidationError('Password must contain at least one special character')
        if not re.search(r"[\d]",value):
            raise serializers.ValidationError('Password must contain at least one digit')
        
        return value
    
    def validate(self, attrs:Dict[str,Any]):
        errors:Dict[str,List[str]] = {}
        if attrs['password'] != attrs['password2']:
            errors.setdefault('password2',[]).append('The passwords do not match')
            raise ValidationError(errors)

        return attrs

    def create(self, validated_data:Dict[str,Any])->User:
        validated_data.pop('password2')
        validated_data['is_active'] = False
        return User.objects.create_user(**validated_data)
    
class UserActivationSerializer(serializers.ModelSerializer):
    
    activation_token = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['activation_token']
        
    def validate(self,attrs:Dict[str,Any]):
        errors:Dict[str,List[str]] = {}
        try:
            attrs['activation_token'] = JWTAuthentication().get_validated_token(attrs['activation_token'])
        except InvalidToken as e:
            errors.setdefault('activation_token',[]).append('The activation token is invalid or expired')
            raise ValidationError(errors)
        return attrs
    
    def activate_user(self)-> User:
        payload = self.validated_data['activation_token'].payload
        
        user = User.objects.get(id=payload['user_id'])
        if not user.is_active:
            user.is_active = True
        user.save()
        return user
    
class UserLoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    
    def __init__(self,*args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields['username'].required = False
    
    def validate(self, attrs:Dict[str,Any]):
        errors:Dict[str,List[str]] = {}
        
        email = attrs.get('email')
        password = attrs.get('password')
        username = attrs.get('username')
        
        if not (email or username):
            errors.setdefault('email_or_username',[]).append('Either email or username is required')
            raise ValidationError(errors)
        
        if email:
            user = User.objects.filter(email=email).first()
        elif username:
            user = User.objects.filter(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                raise AuthenticationFailed('The user is not active')
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
            return attrs
        else:
            raise AuthenticationFailed('Invalid credentials')

class UserRefreshSerializer(TokenRefreshSerializer):
    pass