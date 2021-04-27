from notes_app.models import Notes
from logging_config.logger import get_logger


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
