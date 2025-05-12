from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    role,
    user,
)

router = DefaultRouter()
router.register(f'roles',role.RoleViewSet)
router.register(f'users',user.UserViewSet)

urlpatterns = [
    path('',include(router.urls)),
]