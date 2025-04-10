from typing import Dict,Any,List
from django.core.exceptions import ValidationError
from rest_framework import serializers
from ..models import Profile,Gender
import re

class ProfileCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150,min_length=2)
    second_name = serializers.CharField(max_length=150,min_length=2,required=False)
    last_name = serializers.CharField(max_length=150,min_length=2)
    second_last_name = serializers.CharField(max_length=150,min_length=2,required=False)
    gender_id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Profile
        fields = ('first_name','second_name','last_name','second_last_name','gender_id')
    
    def validate_first_name(self,value:str):
        value = value.strip()
        if not re.match(r'^[A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑa-záéíóúüñ\s]*$',value):
            raise serializers.ValidationError('Firts name must start with a capital letter, and only contain letters and spaces')
        
        return value
    
    def validate_second_name(self,value:str):
        value = value.strip()
        if not re.match(r'^[A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑa-záéíóúüñ\s]*$',value):
            raise serializers.ValidationError('Second name must start with a capital letter, and only contain letters and spaces')
        
        return value
    
    def validate_last_name(self,value:str):
        value = value.strip()
        if not re.match(r'^[A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑa-záéíóúüñ\s]*$',value):
            raise serializers.ValidationError('Last name must start with a capital letter, and only contain letters and spaces')
        
        return value
    
    def validate_second_last_name(self,value:str):
        value = value.strip()
        if not re.match(r'^[A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑa-záéíóúüñ\s]*$',value):
            raise serializers.ValidationError('Second last name must start with a capital letter, and only contain letters and spaces')
        
        return value
    
    def validate_gender_id(self,value:int):
        if not Gender.objects.filter(id=value).exists():
            raise serializers.ValidationError('Gender does not exist')
        return value
    
    def validate(self, attrs:Dict[str,Any]):
        errors:Dict[str,List[str]] = {}
        user_id = self.context['request'].user.id
        if Profile.objects.filter(user_id=user_id).exists():
            errors.setdefault('user_id',[]).append('The user already has a profile')        
        if errors:
            raise ValidationError(errors)
        attrs['user_id'] = user_id
        return attrs
    
    def create(self,validated_data:Dict[str,Any])->Profile:
        return Profile.objects.create(**validated_data)