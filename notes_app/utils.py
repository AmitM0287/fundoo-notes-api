from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

import jwt
from jwt.exceptions import InvalidSignatureError

from notes_app.models import Notes, Labels
from logging_config.logger import get_logger
from auth_app.utils import get_object_by_username


# Configure logger
logger = get_logger()


def get_notes_by_id(id):
    """
        This method is used to get notes according to that id.
        :param id: It's accept id as parameter.
        :return: It's return that object.
    """
    try:
        # Return notes object
        return Notes.objects.get(id=id)
    except Notes.DoesNotExist as e:
        # Raise exception notes does not exist.
        logger.exception(e)
        raise Notes.DoesNotExist


def get_notes_by_user_id(user_id):
    """
        This method is used to get notes according to that user_id.
        :param id: It's accept user id as parameter.
        :return: It's return that object.
    """
    try:
        # Return notes object
        notes = Notes.objects.filter(user_id=user_id)
        if not notes:
            raise Notes.DoesNotExist
        return notes
    except Notes.DoesNotExist as e:
        # Raise exception notes does not exist.
        logger.exception(e)
        raise Notes.DoesNotExist


def varify_token(function):
    """
        This decorator is used to check token is included or not.
        :param function: It's accept function as parameter.
        :return: It's return updated function.
    """
    def wrapper(self, request):
        # Get token from header
        token = request.headers.get('token')
        if not token:
            return Response({'success': False, 'message': 'Please include token!'}, status=status.HTTP_400_BAD_REQUEST)
        return function(self, request, token)
    return wrapper


def get_user_id(token):
    """
        This method is used to get user id from token.
        :param token: It's accept token as parameter.
        :return: It's return user id or raise an exception.
    """
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        # Getting user according to username
        user = get_object_by_username(data.get('username'))
        return user.id
    except InvalidSignatureError as e:
        logger.exception(e)
        raise InvalidSignatureError


def get_labels_by_id(id):
    """
        This method is used to get labels according to that id.
        :param id: It's accept id as parameter.
        :return: It's return that object.
    """
    try:
        # Return notes object
        return Labels.objects.get(id=id)
    except Labels.DoesNotExist as e:
        # Raise exception notes does not exist.
        logger.exception(e)
        raise Labels.DoesNotExist


def get_labels_by_user_id(user_id):
    """
        This method is used to get labels according to that user_id.
        :param id: It's accept user id as parameter.
        :return: It's return that object.
    """
    try:
        # Return notes object
        labels = Labels.objects.filter(user_id=user_id)
        if not labels:
            raise Labels.DoesNotExist
        return labels
    except Labels.DoesNotExist as e:
        # Raise exception notes does not exist.
        logger.exception(e)
        raise Labels.DoesNotExist
