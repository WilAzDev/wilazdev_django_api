from rest_framework import status,viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.authorization.models import Role
from apps.authentication.models import User
from ..permissions import HasRoles
from ..serializers import role,permission
from http import HTTPMethod
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = role.RoleSerializer
    permission_classes = [HasRoles]
    allowed_roles = ['admin']
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='user_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={200: role.RoleSerializer(many=True)},
    )
    @action(
        detail=False,
        methods=[HTTPMethod.GET],
        url_path='users/(?P<user_id>\d+)',
        url_name='roles-user')
    def get_user_roles(self,request,user_id:int):
        user = User.objects.get(pk=user_id)
        roles = user.roles.all()
        serializer = self.get_serializer(roles,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=permission.AssignPermissionSerializer,
        responses={200: openapi.Response('Success',role.RoleSerializer)},
    )
    @action(
        detail=True,
        methods=[HTTPMethod.POST],
        url_path='assign-permission',
    )
    def assign_permission(self,request,pk=True):
        role = self.get_object()
        in_serializer = permission.AssignPermissionSerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)
        permissions = in_serializer.validated_data['permissions']
        
        role.assign_permissions(permissions)
        serializer = self.get_serializer(role)
        return Response(serializer.data,status=status.HTTP_200_OK)
        