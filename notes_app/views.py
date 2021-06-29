from elasticsearch.client import Elasticsearch
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from jwt.exceptions import InvalidSignatureError

from django.conf import settings

from notes_app.serializers import NotesSerializer, LabelsSerializer
from logging_config.logger import get_logger
from notes_app.models import Notes, Labels
from notes_app.utils import get_notes_by_id, get_notes_by_user_id, varify_token, get_labels_by_id, get_labels_by_user_id
from notes_app.elastic_search import ElasticSearch

import xlsxwriter
import pandas


# Logger configuration
logger = get_logger()


class NotesAPIView(APIView):
    """
        NotesAPIView : GET, ADD, UPDATE, DELETE Notes
    """
    @varify_token
    def get(self, request, user_id):
        """
            This method is used to get notes instances according to user id.
            :param request: It's accept user_id as parameter.
            :return: It's return notes instances according to that user id.
        """
        try:
            # Get notes object by user id
            notes = get_notes_by_user_id(user_id)
            # Notes serializer
            serializer = NotesSerializer(notes, many=True)
            # Getting notes from elastic search
            # es = ElasticSearch()
            # es_data = es.get_data(user_id=user_id)
            # data = []
            # for ite in range(len(es_data)):
            #     data.append(es_data[ite]['_source'])
            # Return notes instances
            return Response({'success': True, 'message': 'Getting notes successfully!', 'data': {'notes_list': serializer.data}}, status=status.HTTP_200_OK)
        except Notes.DoesNotExist as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'You do not have any notes!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong! Please try again...'}, status=status.HTTP_400_BAD_REQUEST)

    @varify_token
    def post(self, request, user_id):
        """
            This method is used to create notes instance.
            :param request: It's accept title, description and user id as parameter.
            :return: It's return response that notes succcessfully created or not.
        """
        try:
            # Notes serializer
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Create notes instance
            notes = Notes(title=serializer.data.get('title'), description=serializer.data.get('description'), user_id=user_id)
            notes.save()
            data = serializer.data
            data.update({'id': notes.id})
            # Save data into elastic search
            # es = ElasticSearch()
            # es.save_data(title=serializer.data.get('title'), description=serializer.data.get('description'), user_id=user_id)
            #Success response
            return Response({'success': True, 'message': 'Notes created successfully!', 'data': {'notes_list': data}}, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.exception(e)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
            This method is used to update notes instance.
            :param request: It's accept title, description and notes id as parameter.
            :return: It's return response that notes succcessfully updated or not.
        """
        try:
            # Get notes object by notes id
            notes = get_notes_by_id(request.data.get('id'))
            # Notes serializer
            serializer = NotesSerializer(notes, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # Update data in elastic search
            # es = ElasticSearch()
            # es.update_data(doc_id=request.data.get('id'), es_data={'doc': { 'title': request.data.get('title'), 'description': request.data.get('description')}})
            # Notes updated successfully
            return Response({'success': True, 'message': 'Notes updated successfully!', 'data': {'notes_list': serializer.data}}, status=status.HTTP_202_ACCEPTED)
        except Notes.DoesNotExist:
            # Notes instance does not exist
            return Response({'success': False, 'message': 'Notes does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.exception(e)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class ArchiveNotesAPIView(APIView):
    """
        ArchiveNotesAPIView: Archive & UnArchive notes.
    """
    def post(self, request):
        """
            This method is used for archive & unarchive notes.
            :param request: It's accept note_id as parameter.
            :return: It's return response that notes succcessfully archive or unarchive.
        """
        try:
            note_id = request.data.get('note_id')
            note = get_notes_by_id(id=note_id)
            if note.isArchive == False:
                note.isArchive = True
            else:
                note.isArchive = False
            # Save changes
            note.save()
            return Response({'success': True, 'message': 'Notes isArchive successful!'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong! Please try again...'}, status=status.HTTP_400_BAD_REQUEST)


class TrashNotesAPIView(APIView):
    """
        TrashNotesAPIView: Trash notes $ Restore notes.
    """
    def post(self, request):
        """
            This method is used for trash notes & restore notes.
            :param request: It's accept note_id as parameter.
            :return: It's return response that notes succcessfully trash or restore.
        """
        try:
            note_id = request.data.get('note_id')
            note = get_notes_by_id(id=note_id)
            if note.isTrash == False:
                note.isTrash = True
            else:
                note.isTrash = False
            # Save changes
            note.save()
            return Response({'success': True, 'message': 'Notes isTrash successful!'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong! Please try again...'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteNoteAPIView(APIView):
    """
        DeleteNoteAPIView: Delete notes
    """
    def delete(self, request, *args,**kwargs):
        """
            This method is used to delete notes instance.
            :param **kwargs: It's accept notes id as kargs.
            :return: It's return response that notes succcessfully deleted or not.
        """
        try:
            # Getting id from URL
            id = kwargs['id']
            # Get notes object by notes id
            notes = get_notes_by_id(id)
            # # Delete notes instance
            notes.delete()
            # # Delete notes from elastic search
            # es = ElasticSearch()
            # es.delete_data(doc_id=request.data.get('id'))
            # Notes deleted successfully
            return Response({'success': True, 'message': 'Notes deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except Notes.DoesNotExist:
            # Notes does not exist
            return Response({'success': False, 'message': 'Notes does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class LabelsAPIView(APIView):
    """
        LabelsAPIView : GET, ADD, UPDATE, DELETE Labels
    """
    @varify_token
    def get(self, request, user_id):
        """
            This method is used to get labels instances according to user id.
            :param request: It's accept user_id as parameter.
            :return: It's return labels instances according to that user id.
        """
        try:
            # Get labels object by user id
            labels = get_labels_by_user_id(user_id)
            # Labels serializer
            serializer = LabelsSerializer(labels, many=True)
            # Return labels instances
            return Response({'success': True, 'message': 'Getting labels successfully!', 'data': {'labels': serializer.data}}, status=status.HTTP_200_OK)
        except Labels.DoesNotExist as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'You do not have any labels!'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong! Please try again...'}, status=status.HTTP_400_BAD_REQUEST)
    
    @varify_token
    def post(self, request, user_id):
        """
            This method is used to create labels instance.
            :param request: It's accept name as parameter.
            :return: It's return response that Labels succcessfully created or not.
        """
        try:
            # Labels serializer
            serializer = LabelsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Create labels instance
            labels = Labels(name=serializer.data.get('name'), user_id=user_id)
            labels.save()
            # Labels instance created successfully
            return Response({'success': True, 'message': 'Labels created successfully!', 'data': {'labels': serializer.data}}, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.exception(e)
            return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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
            return Response({'success': True, 'message': 'Labels updated successfully!', 'data': {'labels': serializer.data}}, status=status.HTTP_202_ACCEPTED)
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


class ExcelSheetAPIView(APIView):
    # def post(self, request):
    #     try:
    #         # Create a workbook and add a worksheet.
    #         workbook = xlsxwriter.Workbook('/home/amitm/Desktop/notes.xlsx')
    #         worksheet = workbook.add_worksheet('notes')
    #         data = request.data
    #         keys = list(data.keys())
    #         values = list(data.values())
    #         # Write data into excel sheet
    #         for ite in range(len(keys)):
    #             worksheet.write(0, ite, keys[ite])
    #             worksheet.write(1, ite, values[ite])
    #         workbook.close()
    #         return Response({'success': True, 'message': 'Data inserted successfully into excel sheet!'}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         logger.exception(e)
    #         return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            # data = pandas.read_excel('/home/amitm/Desktop/notes.xlsx')
            # print(request.form['file'])
            data = pandas.read_excel(request.data['file'])
            print(data.to_dict('dict'))
            return Response({'success': True, 'message': 'Get data successfully from excel sheet!'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Oops! Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
