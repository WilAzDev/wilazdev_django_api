from rest_framework import serializers
from ..models import Role
import re

class RoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30,min_length=1)
    class Meta:
        model = Role
        fields = ('__all__')
        
    def validate_name(self,value:str):
        value = re.sub(r'\s+', '_', value.strip().lower())
        if Role.objects.filter(name=value).exists():
            raise serializers.ValidationError('Role already exists')
        elif re.search(r"[!@#$%^&*()+\-=\[\]{}|;:'\",.<>/?`~\\]",value):
            raise serializers.ValidationError("Name can't contain special characters")
        elif re.search(r"[\d]",value):
            raise serializers.ValidationError("Name can't contain numbers")
        return value