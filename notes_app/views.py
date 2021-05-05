from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError

from jwt.exceptions import InvalidSignatureError

from notes_app.serializers import NotesSerializer, LabelsSerializer
from logging_config.logger import get_logger
from notes_app.models import Notes, Labels
from notes_app.utils import get_notes_by_id, get_notes_by_user_id, get_user_id, varify_token, get_labels_by_id, get_labels_by_user_id


# Logger configuration
logger = get_logger()


class NotesCRUD(APIView):
    """
        GET, ADD, UPDATE, DELETE Notes
    """
    @varify_token
    def get(self, request, token):
        """
            This method is used to get notes instances according to user id.
            :param request: It's accept token as parameter.
            :return: It's return notes instances according to that user id.
        """
        try:
            # Getting user id from token
            user_id = get_user_id(token)
            # Get notes object by user id
            notes = get_notes_by_user_id(user_id)
            # Notes serializer
            serializer = NotesSerializer(notes, many=True)
            # Return notes instances
            return Response({'success': True, 'message': 'Getting notes successfully!', 'data': {'notes_list': serializer.data}}, status=status.HTTP_200_OK)
        except Notes.DoesNotExist as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'You do not have any notes! Just create one.'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Invalid token!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong! Please try again...'}, status=status.HTTP_400_BAD_REQUEST)

    @varify_token
    def post(self, request, token):
        """
            This method is used to create notes instance.
            :param request: It's accept title, notes and user id as parameter.
            :return: It's return response that notes succcessfully created or not.
        """
        try:
            # Getting user id from token
            user_id = get_user_id(token)
            # Notes serializer
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Create notes instance
            notes = Notes(title=serializer.data.get('title'), notes=serializer.data.get('notes'), user_id=user_id)
            notes.save()
            # Notes instance created successfully
            return Response({'success': True, 'message': 'Notes created successfully!', 'data':serializer.data}, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.exception(e)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Invalid token!'}, status=status.HTTP_400_BAD_REQUEST)
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
            serializer = NotesSerializer(notes, data=request.data)
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


class LabelsCRUD(APIView):
    """
        GET, ADD, UPDATE, DELETE Labels
    """
    @varify_token
    def get(self, request, token):
        """
            This method is used to get labels instances according to user id.
            :param request: It's accept token as parameter.
            :return: It's return labels instances according to that user id.
        """
        try:
            # Getting user id from token
            user_id = get_user_id(token)
            # Get labels object by user id
            labels = get_labels_by_user_id(user_id)
            # Labels serializer
            serializer = LabelsSerializer(labels, many=True)
            # Return labels instances
            return Response({'success': True, 'message': 'Getting labels successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)
        except Labels.DoesNotExist as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'You do not have any labels! Just create one.'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Invalid token!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong! Please try again...'}, status=status.HTTP_400_BAD_REQUEST)
    
    @varify_token
    def post(self, request, token):
        """
            This method is used to create labels instance.
            :param request: It's accept name as parameter.
            :return: It's return response that Labels succcessfully created or not.
        """
        try:
            # Getting user id from token
            user_id = get_user_id(token)
            # Labels serializer
            serializer = LabelsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Create labels instance
            labels = Labels(name=serializer.data.get('name'), user_id=user_id)
            labels.save()
            # Labels instance created successfully
            return Response({'success': True, 'message': 'Labels created successfully!', 'data':serializer.data}, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.exception(e)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Invalid token!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        """
            This method is used to update labels instance.
            :param request: It's accept labels id and name as parameter.
            :return: It's return response that labels succcessfully updated or not.
        """
        try:
            labels = get_labels_by_id(request.data.get('id'))
            # Labels serializer
            serializer = LabelsSerializer(labels, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # Labels updated successfully
            return Response({'success': True, 'message': 'Labels updated successfully!', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
        except Labels.DoesNotExist:
            # Labels instance does not exist
            return Response({'success': False, 'message': 'Labels does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.exception(e)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
            This method is used to delete labels instance.
            :param request: It's accept labels id as parameter.
            :return: It's return response that labels succcessfully deleted or not.
        """
        try:
            labels = get_labels_by_id(request.data.get('id'))
            # Delete labels instance
            labels.delete()
            # Labels deleted successfully
            return Response({'success': True, 'message': 'Labels deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except Labels.DoesNotExist:
            # Labels does not exist
            return Response({'success': False, 'message': 'Labels does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
