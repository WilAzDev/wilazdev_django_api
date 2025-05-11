# from rest_framework import status,viewsets
# from apps.authorization.models import Role
# from ..permissions import HasRoles
# from ..serializers import role

# class RoleViewSet(viewsets.ModelViewSet):
#     queryset = Role.objects.all()
#     serializer_class = role.RoleSerializer
#     permission_classes = [HasRoles]
#     allowed_roles = ['admin']