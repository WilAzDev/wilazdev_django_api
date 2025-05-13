from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.authorization.models import Permission,Role
from apps.authentication.models import User
from apps.authorization.permissions import HasRoles
from apps.authorization.serializers import permission
from http import HTTPMethod
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = permission.PermissionSerializer
    permission_classes = [HasRoles]
    allowed_roles = ['admin']
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='role_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: permission.PermissionSerializer(many=True)}
    )
    @action(
        detail=False,
        methods=[HTTPMethod.GET],
        url_path='roles/(?P<role_id>\d+)',
        url_name='permissions-rol'
    )
    def get_role_permissions(self,request,role_id:int):
        role = Role.objects.get(id=role_id)
        permissions = role.permissions.all()
        serializer = self.get_serializer(permissions,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='user_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: permission.PermissionSerializer(many=True)}
    )
    @action(
        detail=False,
        methods=[HTTPMethod.GET],
        url_path='users/(?P<user_id>\d+)',
        url_name='permissions-user'
    )
    def get_user_permissions(self,request,user_id:int):
        user = User.objects.get(id=user_id)
        permissions = user.permissions.all()
        serializer = self.get_serializer(permissions,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    