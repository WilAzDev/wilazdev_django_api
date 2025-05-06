from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from ..models import Gender
from ..serializers.gender import GenderSerializer

class GenderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer