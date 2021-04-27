from django.contrib.auth.models import User

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
