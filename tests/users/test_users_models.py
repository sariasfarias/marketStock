import pytest

from users.models import UserProfile


@pytest.mark.django_db
class TestUserProfile:
    def test_create_user(self):
        user = UserProfile.objects.create_user(
            email='test@example.com',
            name='John',
            lastname='Doe',
            password='mypassword'
        )
        assert user.email, 'test@example.com'
        assert user.name, 'John'
        assert user.lastname, 'Doe'
        assert user.check_password('mypassword')

    def test_raise_error_when_empty_email(self):
        with pytest.raises(ValueError):
            UserProfile.objects.create_user(
                email=None,
                name='John',
                lastname='Doe',
                password='mypassword'
            )

    def test_raise_error_when_empty_name(self):
        with pytest.raises(ValueError):
            UserProfile.objects.create_user(
                email='test@example.com',
                name=None,
                lastname='Doe',
                password='mypassword'
            )

    def test_raise_error_when_empty_lastname(self):
        with pytest.raises(ValueError):
            UserProfile.objects.create_user(
                email='test@example.com',
                name='John',
                lastname=None,
                password='mypassword'
            )
