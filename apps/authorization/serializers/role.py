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

class AssignRoleSerializer(serializers.Serializer):
    roles = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=True,
        help_text='List of roles id'        
    )
    
    def validate_roles(self, value):
        existing_ids = set(Role.objects.filter(pk__in=value).values_list('id', flat=True))
        missing = [rid for rid in value if rid not in existing_ids]
        
        if missing:
            if len(missing) == 1:
                msg = f"The rol for id {missing[0]} does not exist"
            else:
                msg = f"The rol for ids {', '.join(map(str, missing))} does not exist"
            raise serializers.ValidationError(msg)
        
        return value