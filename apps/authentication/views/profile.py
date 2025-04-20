from rest_framework.permissions import IsAuthenticated
from rest_framework import (
    generics,
)
from ..serializers.profile import (
    ProfileCreateSerializer,
    ProfileUpdateSerializer
)
from ..models import Profile

class ProfileCreateView(generics.CreateAPIView):
    serializer_class = ProfileCreateSerializer
    permission_classes = [IsAuthenticated]
    
class ProfileUpdateView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]