from rest_framework import status
from rest_framework.response import Response

from dotenv import dotenv_values
import jwt


# Configure .env values
config = dotenv_values('.env')

# JWT SECRET KEY
JWT_SECRET_KEY = config.get('JWT_SECRET_KEY')


def get_token(data):
    """
        Get token
    """
    token = jwt.encode(data, JWT_SECRET_KEY, algorithm="HS256")
    return Response({'Token': token}, status=status.HTTP_200_OK)


def validate_token(token):
    """
        Validate that token
    """
    data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    return Response({'Data': data}, status=status.HTTP_200_OK)
