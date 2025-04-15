from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import (
    generics,
    status
)
from ..serializers.user import (
    UserRegisterSerializer,
    UserActivationSerializer,
)
from ..models import User
from ..functions.token import (
    generate_recovery_token
)
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
        
        token = generate_recovery_token(user)
        
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