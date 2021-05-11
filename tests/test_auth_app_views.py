import pytest
import json
from django.urls import reverse

class TestAuth:
    @pytest.mark.django_db
    def test_login_api(self, client, django_user_model):
        user = django_user_model.objects.create_user(
            username='someone', password='password'
        )
        url = reverse('auth_app:user_login')
        data = {'username':'someone', 'password':'password'}
        response = client.post(url, data)
        assert response.status_code == 200
        op = json.loads(response.content)
        assert op['data']['username'] == 'someone'
