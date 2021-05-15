from django.contrib.auth.models import User
from django.http import response
import pytest
import json
from django.urls import reverse
import jwt
from notes_app.models import Notes


class TestNotesAPI:
    """
        Test Notes API
    """
    @pytest.mark.django_db
    def test_response_as_create_notes_successfully(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(id=1, username='Minu', password='1234')
        user.save()
        url = reverse('auth_app:user_login')
        # Login successful
        data = {'username':'Minu', 'password':'1234'}
        response = client.post(url, data)
        json_data = json.loads(response.content)
        token = json_data['data']['token']
        # Create notes
        url = reverse('notes_app:notes_crud')
        data = {'id':1, 'title':'Python programming', 'description':'Python is the most popular language now days.', 'user_id':1}
        header = {'HTTP_TOKEN': token}
        response = client.post(url, data, **header)
        json_data = json.loads(response.content)
        assert response.status_code == 200
        assert json_data['data']['notes_list']['title'] == 'Python programming'

    @pytest.mark.django_db
    def test_response_as_validation_error_while_create_notes(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(id=1, username='Minu', password='1234')
        user.save()
        url = reverse('auth_app:user_login')
        # Login successful
        data = {'username':'Minu', 'password':'1234'}
        response = client.post(url, data)
        json_data = json.loads(response.content)
        token = json_data['data']['token']
        # Create notes
        url = reverse('notes_app:notes_crud')
        data = {'title':'', 'description':'', 'id':1}
        header = {'HTTP_TOKEN': token}
        response = client.post(url, data, **header)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_get_notes_successfully(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(id=1, username='Minu', password='1234')
        user.save()
        url = reverse('auth_app:user_login')
        # Login successful
        data = {'username':'Minu', 'password':'1234'}
        response = client.post(url, data)
        json_data = json.loads(response.content)
        token = json_data['data']['token']
        # Create notes
        url = reverse('notes_app:notes_crud')
        data = {'id':1, 'title':'Python programming', 'description':'Python is the most popular language now days.', 'user_id':1}
        header = {'HTTP_TOKEN': token}
        response = client.post(url, data, **header)
        json_data = json.loads(response.content)
        assert response.status_code == 200
        assert json_data['data']['notes_list']['title'] == 'Python programming'
        # Get notes
        url = reverse('notes_app:notes_crud')
        header = {'HTTP_TOKEN': token}
        response = client.get(url, **header)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_response_as_update_notes_successfully(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(id=1, username='Minu', password='1234')
        user.save()
        url = reverse('auth_app:user_login')
        # Login successful
        data = {'username':'Minu', 'password':'1234'}
        response = client.post(url, data)
        json_data = json.loads(response.content)
        token = json_data['data']['token']
        # Create notes
        url = reverse('notes_app:notes_crud')
        data = {'title':'Python programming', 'description':'Python is the most popular language now days.'}
        header = {'HTTP_TOKEN': token}
        response = client.post(url, data, **header)
        json_data = json.loads(response.content)
        note_id = json_data['data']['notes_list']['id']
        assert response.status_code == 200
        assert json_data['data']['notes_list']['title'] == 'Python programming'
        # Update notes
        url = reverse('notes_app:notes_crud')
        data = json.dumps({'id':note_id, 'title':'Django', 'description':'Django is the most popular framework now days.'})
        response = client.put(url, data, content_type='application/json')
        json_data = json.loads(response.content)
        assert response.status_code == 202

    @pytest.mark.django_db
    def test_response_as_delete_notes_successfully(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(id=1, username='Minu', password='1234')
        user.save()
        url = reverse('auth_app:user_login')
        # Login successful
        data = {'username':'Minu', 'password':'1234'}
        response = client.post(url, data)
        json_data = json.loads(response.content)
        token = json_data['data']['token']
        # Create notes
        url = reverse('notes_app:notes_crud')
        data = {'title':'Python programming', 'description':'Python is the most popular language now days.'}
        header = {'HTTP_TOKEN': token}
        response = client.post(url, data, **header)
        json_data = json.loads(response.content)
        note_id = json_data['data']['notes_list']['id']
        assert response.status_code == 200
        assert json_data['data']['notes_list']['title'] == 'Python programming'
        # Delete notes
        url = reverse('notes_app:notes_crud')
        data = {'id':note_id}
        data = json.dumps(data)
        response = client.delete(url, data, content_type='application/json')
        assert response.status_code == 204
