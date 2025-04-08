from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import (
    generics,
    status
)
from .serializers import (
    UserRegisterSerializer,
)

# Create your views here.
class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    authentication_classes = []
    
    def create(self,*args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message':'El usuario fue creado con exito'},status=status.HTTP_201_CREATED)