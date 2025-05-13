from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    role,
    user,
    permission
)

router = DefaultRouter()
router.register(f'roles',role.RoleViewSet)
router.register(f'users',user.UserViewSet)
router.register(f'permissions',permission.PermissionViewSet)

urlpatterns = [
    path('',include(router.urls)),
]