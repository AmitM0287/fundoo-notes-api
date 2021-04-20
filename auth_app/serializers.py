from rest_framework import serializers
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """
        User Register Serializer
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password']


class UserLoginSerializer(serializers.ModelSerializer):
    """
        User Login Serializer
    """
    class Meta:
        model = User
        fields = ['username', 'password']
