from django.contrib.auth.models import User


def get_user_instance(id):
        """
            This method is used to return user instance according to user id.
            :param id: It's accept user id as parameter.
            :return: It's return user instance or raise an exception.
        """
        try:
            # Return user instance
            return User.objects.get(id=id)
        except User.DoesNotExist as e:
            # Raise exception user does not exist.
            logger.exception(e)
            raise User.DoesNotExist
