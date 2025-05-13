from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers import user,role,permission
from apps.authentication.models import User
from apps.authorization.permissions import HasRoles
from http import HTTPMethod
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class UserViewSet(viewsets.GenericViewSet):
    serializer_class = user.UserSerializer
    queryset = User.objects.all()
    permission_classes = [HasRoles]
    allowed_roles = ['admin']
    allow_safe_methods = False
    
    @action(
        detail=True,
        methods=[HTTPMethod.GET],
        url_path='toogle')
    def toogle(self, request, pk=None):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=role.AssignRoleSerializer,
        responses={200: openapi.Response('Success', user.UserSerializer)}
    )
    @action(
        detail=True,
        methods=[HTTPMethod.POST],
        url_path='assign-roles')
    def assign_roles(self, request, pk=None):
        user = self.get_object()
        in_serializer = role.AssignRoleSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        roles = in_serializer.validated_data['roles']
        
        user.assign_roles(roles)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=permission.AssignPermissionSerializer,
        responses={200: openapi.Response('Success',user.UserSerializer)},
    )
    @action(
        detail=True,
        methods=[HTTPMethod.POST],
        url_path='assign-permission',
    )
    def assign_permission(self,request,pk=True):
        user = self.get_object()
        in_serializer = permission.AssignPermissionSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        permissions = in_serializer.validated_data['permissions']
        
        user.assign_permissions(permissions)
        serializer = self.get_serializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    
        
    