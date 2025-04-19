from rest_framework.permissions import IsAuthenticated
from rest_framework import (
    generics,
)
from ..serializers.profile import (
    ProfileCreateSerializer
)

class ProfileCreateView(generics.CreateAPIView):
    serializer_class = ProfileCreateSerializer
    permission_classes = [IsAuthenticated]
    
    