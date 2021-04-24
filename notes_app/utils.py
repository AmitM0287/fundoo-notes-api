from notes_app.models import Notes


def get_instance_user_id(user_id):
        """
            This method is used to get notes instance according to user id.
            :param user_id: It's accept user id as parameter.
            :return: It's return notes instances or raise an exception.
        """
        try:
            # Return notes instances
            notes = Notes.objects.filter(user_id=user_id)
            if not notes:
                raise Notes.DoesNotExist
            return list(notes)
        except Notes.DoesNotExist as e:
            # Raise exception user does not exist.
            logger.exception(e)
            raise Notes.DoesNotExist


def get_instance_notes_id(notes_id):
        """
            This method is used to get notes instance according to notes id.
            :param user_id: It's accept notes id as parameter.
            :return: It's return notes instance or raise an exception.
        """
        try:
            # Return notes instance
            return Notes.objects.get(id=notes_id)
        except Notes.DoesNotExist as e:
            # Raise exception notes does not exist.
            logger.exception(e)
            raise Notes.DoesNotExist
