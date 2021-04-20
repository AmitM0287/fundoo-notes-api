from logging_configuration.logging_config import get_logger
from django.contrib.auth.models import User, auth
from .serializers import UserLoginSerializer, UserRegisterSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Get logger to put exceptions into exceptions.log file
logger = get_logger()


class UserLogin(APIView):
    """
        User Login View
    """
    def post(self, request, format=None):
        try:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid()
            user = auth.authenticate(username=serializer.data.get('username'), password=serializer.data.get('password'))
            if user is not None: 
                return Response({'Message': 'Login successfull!'}, status=status.HTTP_200_OK)
            else:
                return Response({'Message': 'Login failed!'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.exception(e)
            return Response({'Message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class UserRegister(APIView):
    """
        User Register View
    """
    def post(self, request, format=None):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                if User.objects.filter(email=serializer.data.get('email')).exists():
                    return Response({'Message': 'A user with that email already exists.'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    user = User.objects.create_user(first_name=serializer.data.get('first_name'), last_name=serializer.data.get('last_name'), email=serializer.data.get('email'), username=serializer.data.get('username'), password=serializer.data.get('password'))
                    user.save()
                    return Response({'Message': 'Registration successfull!'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.exception(e)
            return Response({'Message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
