import datetime
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

def generate_recovery_token(user,minutes):
    
    token = AccessToken.for_user(user)
    
    token.set_exp(from_time=datetime.datetime.now(),lifetime=datetime.timedelta(minutes=minutes))
    
    return str(token)

def is_token_valid(token):
    
    try:
        token_backed = TokenBackend(
            algorithm=api_settings.ALGORITHM,
            signing_key=api_settings.SIGNING_KEY
        )
        payload = token_backed.decode(token,verify=True)
        
        outstanding_token = OutstandingToken.objects.get(
            token=token,
            user_id = payload['user_id']
        )
        
        if BlacklistedToken.objects.filter(token=outstanding_token).exists():
            return False
        return True
    except (InvalidToken,TokenError):
        return False