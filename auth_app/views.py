from logging_configuration.logging_config import get_logger
from auth_app.serializers import UserLoginSerializer, UserRegisterSerializer, UserUpdateSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User, auth


# Get logger to put exceptions into exceptions.log file
logger = get_logger()


class UserLogin(APIView):
    """
        Authenticate User instance
    """
    def post(self, request, format=None):
        try:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid()
            user = auth.authenticate(username=serializer.data.get('username'), password=serializer.data.get('password'))
            if user is not None: 
                return Response({'message': 'Login successfull!'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Login failed!'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class UserRegister(APIView):
    """
        Create a User instance
    """
    def post(self, request, format=None):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                if User.objects.filter(email=serializer.data.get('email')).exists():
                    return Response({'message': 'A user with that email already exists.'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    user = User.objects.create_user(first_name=serializer.data.get('first_name'), last_name=serializer.data.get('last_name'), email=serializer.data.get('email'), username=serializer.data.get('username'), password=serializer.data.get('password'))
                    user.save()
                    return Response({'message': 'Registration successfull!'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class UserUpdate(APIView):
    """
        Update a User instance
    """
    def put(self, request, id, format=None):
        try:
            user =  User.objects.get(id=id)
            serializer = UserUpdateSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    """
        Reset password of a User instance
    """
    def put(self, request, id, format=None):
        try:
            user = User.objects.get(id=id)
            user.set_password(request.data.get('password'))
            user.save()
            return Response({'message': 'New password is created!'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class UserDelete(APIView):
    """
        Delete a User instance
    """
    def delete(self, request, id, format=None):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response({'message': 'User deleted successfully!', 'username': user.username}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
