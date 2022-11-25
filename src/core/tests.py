from django.test import Client
from rest_framework.test import APITestCase

from core.models import User
from core.serializers import LoginSerializer

c = Client()


class UserTestCase(APITestCase):

    def test_create_user_serializer(self):
        user_create = User.objects.create(
            username='test_username',
            first_name='test_name',
            last_name='test_last_name',
            is_superuser=False,
            password='test_password123'

        )
        user = str(User.objects.get(username=user_create.username))
        serializer = LoginSerializer(user_create).data
        self.assertEqual(serializer['username'], user)

    def test_update_password(self):
        user_create = c.post(
            '/core/signup',
            {
                'username': 'test_username',
                'first_name': 'test_name',
                'last_name': 'test_last_name',
                'email': 'test_email@test.com',
                'is_superuser': False,
                'password': 'test_password123',
                'password_repeat': 'test_password123'
            }
        )

        auth = c.post('/core/login', {'username': 'test_username',
                                      'password': 'test_password123'})

        user_update = c.put(
            '/core/profile',
            {
                'username': 'test_username_2',
                'first_name': 'test_first_name_2',
                'last_name': 'test_last_name_2',
                'email': 'test_email_2@test.com'
            },
            content_type='application/json'
        )

        self.assertNotEqual(user_update.data['username'], user_create.data['username'], 'invalid update first_name')
        self.assertNotEqual(user_update.data['first_name'], user_create.data['first_name'], 'invalid update first_name')
        self.assertNotEqual(user_update.data['last_name'], user_create.data['last_name'], 'invalid update last_name')
        self.assertNotEqual(user_update.data['email'], user_create.data['email'], 'invalid update email')
