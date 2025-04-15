from django.urls import path
from .views import (
    user,
    profile
)
urlpatterns = [
    path('register',user.UserRegisterView.as_view(),name='auth_register'),
    path('activate',user.UserActivationView.as_view(),name='auth_activate'),
    path('profile/create',profile.ProfileCreateView.as_view(),name='auth_profile_create')
]