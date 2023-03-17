from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import UserProfile
from .serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)