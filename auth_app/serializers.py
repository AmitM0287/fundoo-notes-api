from rest_framework import serializers

from django.contrib.auth.models import User


class LoginSerializer(serializers.ModelSerializer):
    """
        Login Serializer : username, password
    """
    username = serializers.CharField(min_length=2, max_length=20, required=True)
    password = serializers.CharField(min_length=4, max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterSerializer(serializers.ModelSerializer):
    """
        Register Serializer : first_name, last_name, email, username, password
    """
    first_name = serializers.CharField(min_length=2, max_length=20, required=True)
    last_name = serializers.CharField(min_length=2, max_length=20, required=True)
    email = serializers.EmailField(min_length=4, max_length=30, required=True)
    username = serializers.CharField(min_length=2, max_length=20, required=True)
    password = serializers.CharField(min_length=4, max_length=30, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class UsernameSerializer(serializers.ModelSerializer):
    """
        Username Serializer : username
    """
    username = serializers.CharField(min_length=2, max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username']
