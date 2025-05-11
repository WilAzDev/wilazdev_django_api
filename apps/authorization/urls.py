from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    role
)

router = DefaultRouter()
# router.register(f'roles',role.RoleViewSet)

urlpatterns = [
    # path('',include(router.urls)),
]