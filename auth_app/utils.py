from django.contrib.auth.models import User
from django.conf import settings

from logging_config.logger import get_logger


# Configure logger
logger = get_logger()


def get_object_by_id(id):
    """
        This method is used to get object according to that id.
        :param id: It's accept id as parameter.
        :return: It's return that object.
    """
    try:
        return User.objects.get(id=id)
    except User.DoesNotExist as e:
        logger.exception(e)
        raise User.DoesNotExist


def get_object_by_username(username):
    """
        This method is used to get object according to that username.
        :param id: It's accept username as parameter.
        :return: It's return that object.
    """
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist as e:
        logger.exception(e)
        raise User.DoesNotExist


def get_cache(key):
    """
        This method is used to get cache value according to that key.
        :param key: It's accept key as parameter.
        :return: It's return value according to that key.
    """
    return settings.CACHE.get(key)


def set_cache(key, value):
    """
        This method is used to set cache according to key and value.
        :param key: It's accept key as parameter.
        :param value: It's accept value as another parameter.
        :return: None
    """
    settings.CACHE.set(key, value)
