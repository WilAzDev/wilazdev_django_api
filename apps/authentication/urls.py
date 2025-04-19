from django.urls import path
from .views import (
    user,
    profile
)
urlpatterns = [
    path('register',user.UserRegisterView.as_view(),name='auth_register'),
    path('login',user.UserLoginView.as_view(),name="auth_login"),
    path('logout', user.UserLogoutView.as_view(),name="auth_logout"),
    path('refresh',user.UserRefreshView.as_view(),name='auth_refresh'),
    path('activate',user.UserActivationView.as_view(),name='auth_activate'),
    path('profile/create',profile.ProfileCreateView.as_view(),name='auth_profile_create')
]