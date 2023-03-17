from rest_framework import serializers

from users.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', 'lastname', 'email', 'password']
