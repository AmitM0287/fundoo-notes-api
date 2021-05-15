import pytest
import json
from django.urls import reverse


class TestLoginAPI:
    """
        Test Login API
    """
    @pytest.mark.django_db
    def test_response_as_login_succssful(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Minu', password='7777')
        user.save()
        url = reverse('auth_app:user_login')
        # Login successful
        data = {'username':'Minu', 'password':'7777'}
        response = client.post(url, data)
        assert response.status_code == 200
        json_data = json.loads(response.content)
        assert json_data['data']['username'] == 'Minu'

    @pytest.mark.django_db
    def test_response_as_login_failed(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Minu', password='7777')
        user.save()
        url = reverse('auth_app:user_login')
        # Login failed
        data = {'username':'Minu', 'password':'1234'}
        response = client.post(url, data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_validation_error(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Minu', password='7777')
        user.save()
        url = reverse('auth_app:user_login')
        # Validation error
        data = {'username':'Minu', 'password':''}
        response = client.post(url, data)
        assert response.status_code == 400


class TestRegisterAPI:
    """
        Test Register API
    """
    @pytest.mark.django_db
    def test_response_as_email_is_already_exist(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(first_name='Amit', last_name='Manna', email='amitmanna0287@gmail.com', username='AmitM0287', password='1234')
        user.save()
        url = reverse('auth_app:user_register')
        # Email is already exist
        data = {'first_name': 'Amit', 'last_name': 'Manna', 'email': 'amitmanna0287@gmail.com', 'username': 'AmitM0287', 'password': '1234'}
        response = client.post(url, data)
        assert response.status_code == 400
    
    @pytest.mark.django_db
    def test_response_as_username_is_already_exist(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(first_name='Amit', last_name='Manna', email='amitmanna0287@gmail.com', username='AmitM0287', password='1234')
        user.save()
        url = reverse('auth_app:user_register')
        # Username is already taken
        data = {'first_name': 'Amit', 'last_name': 'Manna', 'email': 'amitmanna950@gmail.com', 'username': 'AmitM0287', 'password': '1234'}
        response = client.post(url, data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_registration_successful(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(first_name='Amit', last_name='Manna', email='amitmanna0287@gmail.com', username='AmitM0287', password='1234')
        user.save()
        url = reverse('auth_app:user_register')
        # Registration succesfull
        data = {'first_name': 'Minu', 'last_name': 'Manna', 'email': 'minu0287@gmail.com', 'username': 'Minu0287', 'password': '7777'}
        response = client.post(url, data)
        assert response.status_code == 200
        json_data = json.loads(response.content)
        assert json_data['data']['username'] == 'Minu0287'

    @pytest.mark.django_db
    def test_response_as_validation_error(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(first_name='Amit', last_name='Manna', email='amitmanna0287@gmail.com', username='AmitM0287', password='1234')
        user.save()
        url = reverse('auth_app:user_register')
        # Validation error
        data = {'first_name': 'M', 'last_name': 'M', 'email': 'm@gmail.com', 'username': 'M', 'password': '7'}
        response = client.post(url, data)
        assert response.status_code == 400

class TestResetUsernameAPI:
    """
        Test Reset Username API
    """
    @pytest.mark.django_db
    def test_response_as_reset_username_successfully(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(id=1, username='Amit')
        user.save()
        url = reverse('auth_app:user_reset_username')
        # Username updated successfully
        data = json.dumps({'id':1, 'username':'AmitM0287'})
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == 200
        json_data = json.loads(response.content)
        assert json_data['data']['username'] == 'AmitM0287'

    @pytest.mark.django_db
    def test_response_as_user_does_not_exist(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(id=1, username='Amit', password='1234')
        user.save()
        url = reverse('auth_app:user_reset_username')
        # User does not exist
        data = json.dumps({'id':2, 'username':'AmitM'})
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == 400
    
    @pytest.mark.django_db
    def test_response_as_validation_error(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(id=1, username='Amit', password='1234')
        user.save()
        url = reverse('auth_app:user_reset_username')
        # Validation error
        data = json.dumps({'id':1, 'username':'A'})
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == 400


class TestResetPasswordAPI:
    """
        Test Reset Password API
    """
    @pytest.mark.django_db
    def test_response_as_reset_password_successfully(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Minu', password='1234')
        user.save()
        url = reverse('auth_app:user_reset_password')
        # Reset password successfully
        data = json.dumps({'username':'Minu', 'password':'7777'})
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == 200
        json_data = json.loads(response.content)
        assert json_data['data']['username'] == 'Minu'

    @pytest.mark.django_db
    def test_response_as_user_does_not_exist(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Minu', password='1234')
        user.save()
        url = reverse('auth_app:user_reset_password')
        # User does not exist
        data = json.dumps({'username':'Amit', 'password':'7777'})
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_validation_error(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Minu', password='1234')
        user.save()
        url = reverse('auth_app:user_reset_password')
        # Validation error
        data = json.dumps({'username':'Minu', 'password':'7'})
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == 400


class TestUserDeleteAPI:
    """
        Test User Delete API
    """
    @pytest.mark.django_db
    def test_response_as_user_deleted_successfully(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Minu', password='1234')
        user.save()
        url = reverse('auth_app:user_delete')
        # Reset password successfully
        data = json.dumps({'username':'Minu'})
        response = client.delete(url, data, content_type='application/json')
        assert response.status_code == 200
        json_data = json.loads(response.content)
        assert json_data['data']['username'] == 'Minu'

    @pytest.mark.django_db
    def test_response_as_user_does_not_exist(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Minu', password='1234')
        user.save()
        url = reverse('auth_app:user_delete')
        # User does not exist
        data = json.dumps({'username':'Amit'})
        response = client.delete(url, data, content_type='application/json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_validation_error(self, client, django_user_model):
        # Create user
        user = django_user_model.objects.create_user(username='Minu', password='1234')
        user.save()
        url = reverse('auth_app:user_delete')
        # Validation error
        data = json.dumps({'username':'M'})
        response = client.delete(url, data, content_type='application/json')
        assert response.status_code == 400


# class TestVerifyEmailAPI:
#     """
#         Test Verify Email
#     """
