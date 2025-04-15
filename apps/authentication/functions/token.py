import datetime
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings

def generate_recovery_token(user):
    
    token = AccessToken.for_user(user)
    
    token.set_exp(from_time=datetime.datetime.now(),lifetime=datetime.timedelta(minutes=30))
    
    return str(token)