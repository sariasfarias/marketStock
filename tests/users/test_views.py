import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import UserProfile


@pytest.mark.django_db
class TestViews:
    def setup(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        UserProfile.objects.create_user(
            email='test2@example.com',
            name='John',
            lastname='Doe',
            password='mypassword'
        )

    def test_register_user_view(self):
        valid_payload = {
            'name': 'John',
            'lastname': 'Smith',
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(self.register_url, data=valid_payload)
        assert response.status_code == status.HTTP_201_CREATED

    def test_register_with_bad_email(self):
        valid_payload = {
            'name': 'John',
            'lastname': 'Smith',
            'email': 'test',
            'password': 'testpassword',
        }
        response = self.client.post(self.register_url, data=valid_payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_user_view(self):

        valid_payload = {
            'email': 'test2@example.com',
            'password': 'mypassword'
        }
        response = self.client.post(self.login_url, data=valid_payload)
        assert response.status_code == status.HTTP_200_OK

    def test_login_with_bad_credentials(self):

        valid_payload = {
            'email': 'test2@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data=valid_payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
