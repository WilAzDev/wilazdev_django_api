from rest_framework import serializers
from ..models import Permission
import re

class PermissionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=60,min_length=1)
    class Meta:
        model = Permission
        fields = '__all__'

    def validate_name(self, value):
        value = re.sub(r'\s+', '_', value.strip().lower())
        if Permission.objects.filter(name=value).exists():
            raise serializers.ValidationError('Permission already exists')
        elif re.search(r"[!@#$%^&*()+\-=\[\]{}|;:'\",.<>/?`~\\]",value):
            raise serializers.ValidationError("Name can't contain special characters")
        elif re.search(r"[\d]",value):
            raise serializers.ValidationError("Name can't contain numbers")
        return value

class AssignPermissionSerializer(serializers.Serializer):
    permissions = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=True,
        help_text='List of permissions id'        
    )
    
    def validate_permissions(self, value):
        existing_ids = set(Permission.objects.filter(pk__in=value).values_list('id',flat=True))
        missing = [rid for rid in value if rid not in existing_ids]
        
        if missing:
            if len(missing) == 1:
                msg = f"Permission with id {missing[0]} does not exist"
            else:
                msg = f"Permissions with ids {', '.join(map(str,missing))} do not exist"
            raise serializers.ValidationError(msg)
        return value