from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError

from notes_app.serializers import NotesSerializer, UpdateSerializer
from logging_config.logger import get_logger
from notes_app.models import Notes
from notes_app.utils import get_notes_by_id, get_notes_by_user_id

from django.conf import settings
import jwt

# Logger configuration
logger = get_logger()


class NotesCRUD(APIView):
    def get(self, request):
        """
            This method is used to get notes instances according to user id.
            :param request: It's accept user id as parameter.
            :return: It's return notes instances according to that user id.
        """
        try:
            # token = request.headers.get('Authorization')
            # decode = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            # Get notes object by user id
            notes = get_notes_by_user_id(request.data.get('user_id'))
            # Notes serializer
            serializer = NotesSerializer(notes, many=True)
            # Return notes instances
            return Response({'success': True, 'message': 'Getting user notes successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)
        except Notes.DoesNotExist as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'User id does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong! Please try again...'}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        """
            This method is used to create notes instance.
            :param request: It's accept title, notes and user id as parameter.
            :return: It's return response that notes succcessfully created or not.
        """
        try:
            # Notes serializer
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # Notes instance created successfully
            return Response({'success': True, 'message': 'Notes created successfully!', 'data':serializer.data}, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.exception(e)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
            This method is used to update notes instance.
            :param request: It's accept title, notes and notes id as parameter.
            :return: It's return response that notes succcessfully updated or not.
        """
        try:
            notes = get_notes_by_id(request.data.get('id'))
            # Notes serializer
            serializer = UpdateSerializer(notes, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # Notes updated successfully
            return Response({'success': True, 'message': 'Notes updated successfully!', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
        except Notes.DoesNotExist:
            # Notes instance does not exist
            return Response({'success': False, 'message': 'Notes does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.exception(e)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
            This method is used to delete notes instance.
            :param request: It's accept notes id as parameter.
            :return: It's return response that notes succcessfully deleted or not.
        """
        try:
            notes = get_notes_by_id(request.data.get('id'))
            # Delete notes instance
            notes.delete()
            # Notes deleted successfully
            return Response({'success': True, 'message': 'Notes deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except Notes.DoesNotExist:
            # Notes does not exist
            return Response({'success': False, 'message': 'Notes does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
