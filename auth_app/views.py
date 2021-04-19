from django.http import JsonResponse
from logging_configuration.logging_config import get_logger
from django.views import View
from django.contrib.auth.models import User, auth


# Get logger to put exceptions into exceptions.log file
logger = get_logger()


"""
    UserLogin  
"""
class UserLogin(View):
    def post(self, request, *args, **kwargs):
        try:
            # Taking inputs from user
            username = request.POST['username']
            password = request.POST['password']
            # Authenticate username and password
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                return JsonResponse({'Status': 200, 'Message': 'User successfully logged in!'})
            else:
                return JsonResponse({'Status': 200, 'Message': 'User does not exist!'})
        except Exception as e:
            logger.exception(e)
            return JsonResponse({'Status': 'NA', 'Message': 'Oops! Something went wrong. Please try again...'})


"""
    UserRegistration
"""
class UserRegistration(View):
    def post(self, request, *args, **kwargs):
        try:
            # Taking inputs from user
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            # Check weather the username is already taken or not
            if User.objects.filter(username=username).exists():
                return JsonResponse({'Status': 200, 'Message': 'Username is already taken! Try another one...'})
            # Check the email is already taken or not
            elif User.objects.filter(email=email).exists():
                return JsonResponse({'Status': 200, 'Message': 'Email is already taken! Try another one...'})
            else:
                # Create a new user
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.save()
                return JsonResponse({'Status':200, 'Message': 'User registered successfully!'})
        except Exception as e:
            logger.exception(e)
            return JsonResponse({'Status': 'NA', 'Message': 'Oops! Something went wrong. Please try again...'})
