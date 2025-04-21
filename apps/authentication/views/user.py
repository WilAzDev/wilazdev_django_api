from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import (
    generics,
    status
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from rest_framework.permissions import IsAuthenticated
from ..serializers.user import (
    UserRegisterSerializer,
    UserActivationSerializer,
    UserLoginSerializer,
    UserRefreshSerializer,
    UserUpdateSerializer,
    UserRequestChangePasswordSerializer,
    UserChangePasswordSerializer
)
from ..models import User
from ..functions.token import (
    generate_recovery_token
)
from ..choices import PasswordRecoveryChoises
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    authentication_classes = []
    
    def create(self,*args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        email = self.request.data.get('email')
        
        user = User.objects.filter(email=email).first()
        
        token = generate_recovery_token(user,30)
        
        activation_url = f"{settings.FRONTEND_URL}/auth/activate/{token}"
        
        subject = "Activate your account"
        
        from_email = settings.DEFAULT_FROM_EMAIL
        
        recipient_list = [email]
        
        email_content = f'¡Hi {user.username}! Your acount is ready to be activated. Please click on the button below to activate it.'
        text_alternative = f'¡Hi {user.username}! Your acount is ready to be activated. Please click on the next link: {activation_url}.'
        
        html_content = render_to_string(
            'emails/request_email.html',
            {
                'title':subject,
                'frontend_url': activation_url,
                'email_content': email_content,
                'action':subject.split(' ')[0].capitalize()
            }
        )
        
        try:
            msg = EmailMultiAlternatives(subject,text_alternative,from_email,recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            return Response({"error": f'Error sending email: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message':'User created successfully',
            },
        status=status.HTTP_201_CREATED)
        
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
        
class UserActivationView(generics.CreateAPIView):
    serializer_class = UserActivationSerializer
    authentication_classes = []
    
    def create(self,*args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate_user()
        return Response({
            "message":'User activated successfully'
            }, 
        status=status.HTTP_200_OK)
        
class GetTokenView:
    def post(self,request,*args,**kwargs):
        response = super().post(request,*args, **kwargs)
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')
        token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        refresh_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        expires_in = int(token_lifetime.total_seconds())
        refresh_expires_in = int(refresh_lifetime.total_seconds())
        
        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': expires_in,
            'refresh_expires_in': refresh_expires_in,
            'token_type':'Bearer'
        }
        
        return Response(response_data,status=status.HTTP_200_OK)
    
class UserLoginView(GetTokenView,TokenObtainPairView):
    serializer_class = UserLoginSerializer

class UserRefreshView(GetTokenView,TokenRefreshView):
    serializer_class = UserRefreshSerializer    

class UserLogoutView(TokenBlacklistView):
    def post(self,request:Request,*args, **kwargs):
        super().post(request,*args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserRequestChangePasswordView(generics.CreateAPIView):
    serializer_class = UserRequestChangePasswordSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = request.data.get('email')
        
        user = User.objects.filter(email=email).first()
        
        if not user:
            return Response({"message": "Password change request has been sent"}, status=status.HTTP_200_OK)       

        token = generate_recovery_token(user,5)
        
        recovery_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
        
        subject = PasswordRecoveryChoises(request.data.get('motive'))
        
        from_email = settings.DEFAULT_FROM_EMAIL
        
        recipient_list = [email]
        
        email_content = f'¡Hi {user.username}! Your can change your password by clicking in the button bellow.' 
        text_alternative = f'¡Hi {user.username}! Click here to reset your password: {recovery_url}.'

        html_content = render_to_string(
            'emails/request_email.html',
            {
                'title':subject,
                'frontend_url':recovery_url,
                'email_content':email_content,
                'action':subject.split(' ')[0].capitalize()
            }
        )
        
        try:
            msg = EmailMultiAlternatives(subject, html_content, from_email, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            return Response({"error": "Failed to send email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message": "Password change request has been sent"}, status=status.HTTP_200_OK)

class UserChangePasswordView(generics.CreateAPIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = []
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.change_password()
        return Response({'message':'Password changed successfully'},status=status.HTTP_200_OK)
        