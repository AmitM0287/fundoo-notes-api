from logging_configuration.logging_config import get_logger
from .serializers import NotesSerializer
from .models import Notes

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.http import Http404


# Get logger to put exceptions into exceptions.log file
logger = get_logger()


class NotesList(APIView):
    """
        List of all notes, or create a new note.
    """
    def get(self, request, format=None):
        try:
            notes = Notes.objects.all()
            serializer = NotesSerializer(notes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'Message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        try:
            serializer = NotesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Notes created successfully!'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.exception(e)
            return Response({'Message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class NotesDetail(APIView):
    """
        Retrieve a notes instance.
    """
    def get_object(self, pk):
        try:
            return Notes.objects.get(pk=pk)
        except Notes.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        try:
            notes = self.get_object(pk)
            serializer = NotesSerializer(notes)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'Message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
