import json
from datetime import datetime
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import UserProfile
from .serializers import RegisterUserSerializer, LoginUserSerializer
import logging
logger = logging.getLogger(__name__)


class RegisterUserView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(
            f"User Registration at {str(datetime.now())}:"
            f" name={user.name}, lastname={user.lastname}, email={user.email}"
        )


class LoginUserView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        logger.info(
            f"Successful user login at {str(datetime.now())}:"
            f" email={request.data.get('email', None)}"
        )
        return response
