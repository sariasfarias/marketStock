from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import UserProfile


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=UserProfile.objects.all())]
    )

    class Meta:
        model = UserProfile
        fields = ['name', 'lastname', 'email', 'password']
        extra_kwargs = {
            'name': {'required': True},
            'lastname': {'required': True},
            'password': {'write_only': True, 'required': True}
        }

    def validate_password(self, value: str) -> str:
        return make_password(value)


class LoginUserSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['lifetime'] = "{} sec".format(int(refresh.access_token.lifetime.total_seconds()))
        return data
