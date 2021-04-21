from logging_configuration.logging_config import get_logger
from notes_app.serializers import NotesSerializer
from notes_app.models import Notes

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


# Get logger to put exceptions into exceptions.log file
logger = get_logger()


class CreateNotes(APIView):
    """
        Create a Notes instance
    """
    def post(self, request, format=None):
        try:
            serializer = NotesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Notes created successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateNotes(APIView):
    """
        Update a Notes instance
    """
    def put(self, request, id, format=None):
        try:
            notes = Notes.objects.get(id=id)
            serializer = NotesSerializer(notes, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Notes updated successfully!'}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        except Notes.DoesNotExist:
            return Response({'message': 'Notes does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteNotes(APIView):
    """
        Delete a Notes instance
    """
    def delete(self, request, id, format=None):
        try:
            notes = Notes.objects.get(id=id)
            notes.delete()
            return Response({'message': 'Notes deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except Notes.DoesNotExist:
            return Response({'message': 'Notes does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class ListNotes(APIView):
    """
        Retrieve a Notes instance.
    """
    def get(self, request, id, format=None):
        try:
            notes = Notes.objects.filter(user_id=id)
            serializer = NotesSerializer(list(notes), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Notes.DoesNotExist:
            return Response({'message': 'Notes does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
