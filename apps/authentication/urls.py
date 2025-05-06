from django.urls import path
from .views import (
    user,
    profile,
    gender
)
urlpatterns = [
    path('register',user.UserRegisterView.as_view(),name='auth_register'),
    path('login',user.UserLoginView.as_view(),name="auth_login"),
    path('logout', user.UserLogoutView.as_view(),name="auth_logout"),
    path('refresh',user.UserRefreshView.as_view(),name='auth_refresh'),
    path('activate',user.UserActivationView.as_view(),name='auth_activate'),
    path('password/request-change/', user.UserRequestChangePasswordView.as_view(), name='auth_request_password_change'),
    path('password/change/', user.UserChangePasswordView.as_view(), name='auth_change_password'),
    path('users/update/<int:pk>/',user.UserUpdateView.as_view(),name='auth_user_update'),
    path('profiles/create',profile.ProfileCreateView.as_view(),name='auth_profile_create'),
    path('profiles/update/<int:pk>/',profile.ProfileUpdateView.as_view(),name='auth_profile_update'),
    path('genders',gender.GenderListView.as_view(),name='gender_list')
]