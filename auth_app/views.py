from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from django.conf import settings
from django.contrib.auth.models import User, auth

from logging_config.logger import get_logger
from auth_app.serializers import LoginSerializer, RegisterSerializer, UsernameSerializer
from auth_app.utils import get_object_by_id, get_object_by_username
import jwt


# Logger configuration
logger = get_logger()


class LoginAPIView(APIView):
    """
        Login API View
    """
    def post(self, request):
        """
            This method is used for login authentication.
            :param request: It's accept username and password as parameter.
            :return: It's return response that login is successfull or not.
        """
        try:
            # Login serializer
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Create token
            token = jwt.encode({'username': serializer.data.get('username')}, settings.SECRET_KEY, algorithm='HS256')
            # Authenticate username & password
            user = auth.authenticate(username=serializer.data.get('username'), password=serializer.data.get('password'))
            if user is not None:
                return Response({'success': True, 'message': 'Login successfull!', 'username': serializer.data.get('username'), 'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'message': 'Login failed!', 'username': serializer.data.get('username')}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.exception(e)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong! Please try again...'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    """
        Register API View
    """
    def post(self, request):
        """
            This method is used to create new user instance.
            :param request: It's accept first_name, last_name, email, username and password as parameter.
            :return: It's return response that user created successfully or not.
        """
        try:
            # Register serializer
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Create user instance
            user = User.objects.create_user(first_name=serializer.data.get('first_name'), last_name=serializer.data.get('last_name'), email=serializer.data.get('email'), username=serializer.data.get('username'), password=serializer.data.get('password'))
            user.save()
            return Response({'success': True, 'message': 'Registration successfull!', 'username': serializer.data.get('first_name')}, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.exception(e)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong! Please try again...'}, status=status.HTTP_400_BAD_REQUEST)


class ResetUsernameAPIView(APIView):
    """
        Reset Username API View
    """
    def put(self, request):
        """
            This method is used to update username of user instance.
            :param request: It's accept id, username as parameter.
            :return: It's return response that username successfully updated or not.
        """
        try:
            # Username serializer
            serializer = UsernameSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Get user instance according to id
            user = get_object_by_id(request.data.get('id'))
            # Reset username
            user.username = serializer.data.get('username')
            user.save()
            return Response({'success': True, 'message': 'Reset username successfully!', 'username': serializer.data.get('username')}, status=status.HTTP_200_OK)
        except User.DoesNotExist as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'User does not exist!', 'username': serializer.data.get('username')}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.exception(e)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong! Please try again...'}, status=status.HTTP_400_BAD_REQUEST)
    

class ResetPasswordAPIView(APIView):
    """
        Reset Password API View
    """
    def put(self, request):
        """
            This method is used to reset password for a user instance.
            :param request: It's accept username and password as parameter.
            :return: It's return response that password is updated or not.
        """
        try:
            # Login serializer
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Get user instance according to username
            user = get_object_by_username(serializer.data.get('username'))
            # Reset password
            user.set_password(serializer.data.get('password'))
            user.save()
            return Response({'success': True, 'message': 'Reset password successfully!', 'username': serializer.data.get('username')}, status=status.HTTP_200_OK)
        except User.DoesNotExist as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'User does not exist!', 'username': serializer.data.get('username')}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.exception(e)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong! Please try again...'}, status=status.HTTP_400_BAD_REQUEST)
    

class UserDeleteAPIView(APIView):
    def delete(self, request):
        """
            This method is used to delete user instance.
            :param request: It's accept username as parameter.
            :return: It's return that user is successfully deleted or not.
        """
        try:
            # Username serializer
            serializer = UsernameSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Get user instance according to username
            user = get_object_by_username(serializer.data.get('username'))
            # Delete user instance
            user.delete()
            return Response({'success': True, 'message': 'User deleted successfully!', 'username': serializer.data.get('username')}, status=status.HTTP_200_OK)
        except User.DoesNotExist as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'User does not exist!', 'username': serializer.data.get('username')}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.exception(e)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong! Please try again...'}, status=status.HTTP_400_BAD_REQUEST)
