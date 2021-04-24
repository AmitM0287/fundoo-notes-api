from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
from django.contrib.auth.models import User, auth
from django.core.mail import EmailMessage

from logging_config.logger import get_logger
from auth_app.serializers import UserLoginSerializer, UserRegisterSerializer, UserUpdateSerializer
from auth_app.utils import get_user_instance
import jwt


# Logger configuration
logger = get_logger()


class UserLogin(APIView):
    def post(self, request):
        """
            This method is used for login authentication.
            :param request: It's accept username and password as parameter.
            :return: It's return response that login is successfull or not.
        """
        try:
            # User login serializer
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid()
            # Authenticate username and password
            user = auth.authenticate(username=serializer.data.get('username'), password=serializer.data.get('password'))
            # Check login successfull or not
            if user is not None: 
                # Create token
                auth_token = jwt.encode({'username': user.username}, settings.JWT_SECRET_KEY)
                # Sending email
                # email = EmailMessage(
                #     'Login is successfulll',
                #     auth_token,
                #     'mannaamit296@gmail.com',
                #     ['amitmanna0287@gmail.com']
                # )
                # email.send(fail_silently=False)
                # Login successfull
                return Response({'success': True, 'message': 'Login successfull!', 'username': user.username, 'token': auth_token}, status=status.HTTP_200_OK)
            else:
                # Login failed
                return Response({'success': False, 'message': 'Login failed!', 'username': serializer.data.get('username')}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class UserRegister(APIView):
    def post(self, request):
        """
            This method is used to create new user instance.
            :param request: It's accept first_name, last_name, email, username and password as parameter.
            :return: It's return response that user registration is successfull or not.
        """
        try:
            # User register serializer
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                # Create new user instance
                user = User.objects.create_user(first_name=serializer.data.get('first_name'),last_name=serializer.data.get('last_name'), email=serializer.data.get('email'),username=serializer.data.get('username'), password=serializer.data.get('password'))
                user.save()
                # Registration successfull
                return Response({'success': True, 'message': 'Registration successfull!', 'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)
        except serializer.errors as e:
            # Registration failed
            logger.exception(e)
            return Response({'success': False, 'message': 'Registration failed!'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        """
            This method is used to update username of user instance.
            :param request: It's accept id, username as parameter.
            :return: It's return response that user instance successfully updated or not.
        """
        try:
            # Get user instance accoding to id
            user = get_user_instance(request.data.get('id'))
            # User update serializer
            serializer = UserUpdateSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                # Username update successfull
                return Response({'success': True, 'message': 'Username updated sucessfully!', 'username': serializer.data.get('username')}, status=status.HTTP_202_ACCEPTED)
        except serializer.errors as e:
            # Username update failed
            logger.exception(e)
            return Response({'success': False, 'message': 'Username update failed!', 'username':serializer.data.get('username')}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist as e:
            # Username does not exist
            logger.exception(e)
            return Response({'success': False, 'message': 'Username does not exist!', 'username': serializer.data.get('username')}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
            This method is used to delete user instance.
            :param request: It's accept user id as parameter.
            :return: It's return that user is successfully deleted or not.
        """
        try:
            # Get user instance accoding to id
            user = get_user_instance(request.data.get('id'))
            # Delete user instance
            user.delete()
            # Delete user instance successfull
            return Response({'success': True, 'message': 'User deleted successfully!', 'username': user.username}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            # User does not exist
            return Response({'success': False, 'message': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    """
        This method is used to reset password for a user instance.
        :param request: It's accept id and new password as parameter.
        :return: It's return response that password is updated or not.
    """
    def put(self, request):
        try:
            # Get user instance accoding to id
            user = get_user_instance(request.data.get('id'))
            print(user)
            # Set new password for user instance
            user.set_password(request.data.get('password'))
            user.save()
            # Password reset successfull
            return Response({'success': True, 'message': 'New password is created!', 'username': user.username}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            # User does not exist
            return Response({'success': False, 'message': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
