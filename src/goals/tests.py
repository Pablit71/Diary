from datetime import datetime

from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase

from core.models import User
from core.serializers import LoginSerializer


class SerializerTestCase(APITestCase):
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

    def test_create(self):
        c = Client()
        user_create = c.post(
            '/core/signup',
            {
                'username': 'test_username',
                'first_name': 'test_name',
                'last_name': 'test_last_name',
                'is_superuser': False,
                'password': 'test_password123',
                'password_repeat': 'test_password123'
            }
        )

        auth = c.post('/core/login', {'username': 'test_username',
                                      'password': 'test_password123'})

        board_create = c.post(
            '/goals/board/create',
            {
                'user': 'test_username',
                'is_deleted': False,
                'title': 'test_board'
            }
        )
        url_board = reverse('board_list')
        response = c.get(url_board)
        self.assertEqual(response.data[0]['title'], board_create.data['title'])
        self.assertEqual(response.data[0]['id'], board_create.data['id'])

        category_create = c.post(
            '/goals/goal_category/create',
            {
                'user': 'test_username',
                'is_deleted': False,
                'title': 'test_category',
                'board': 1
            }
        )
        url_category = reverse('cat_list')
        response = c.get(url_category)
        self.assertEqual(response.data[0]['title'], category_create.data['title'])
        self.assertEqual(response.data[0]['id'], category_create.data['id'])

        goal_create = c.post(
            '/goals/goal/create',
            {
                'user': 'test_username',
                'is_deleted': False,
                'title': 'test_goal',
                'board': 1,
                'description': 'test_description',
                'category': 1,
                'status': 1,
                'priority': 1,
                'due_date': datetime.now()
            }
        )
        url_goal = reverse('goal_list')
        response = c.get(url_goal)
        self.assertEqual(response.data[0]['title'], goal_create.data['title'])
        self.assertEqual(response.data[0]['id'], goal_create.data['id'])

        comment_create = c.post(
            '/goals/goal_comment/create',
            {
                'user': 'test_username',
                'is_deleted': False,
                'title': 'test_comment',
                'board': 1,
                'goal': 1,
                'text': 'test_text'
            }
        )

        url_comment = reverse('comment_list')
        response = c.get(url_comment)
        self.assertEqual(response.data[0]['text'], comment_create.data['text'])
        self.assertEqual(response.data[0]['id'], comment_create.data['id'])
