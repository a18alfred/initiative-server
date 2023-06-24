from core.apps.accounts.models import Account
from core.apps.projects.models import Category, Project, Comment, LikeDislike
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


class LikeDislikeAPIViewsTestCase(APITestCase):
    """
    Тестирование Views API LikeDislike
    """

    def setUp(self):
        """
        Создаём пользователей с разными правами:
        СуперЮзер
        Модератор
        Обычный пользователь
        Обычный пользователь
        """
        self.password = 'TestPass#22'
        url = reverse('accounts:account_login')

        self.super = Account.objects.create_superuser(phone_number='+77771231212', password=self.password)
        self.super.account_profile.first_name = 'first_name'
        self.super.account_profile.middle_name = 'middle_name'
        self.super.account_profile.last_name = 'last_name'
        self.super.account_profile.email = 'email'
        self.super.account_profile.save()
        resp = self.client.post(url, {'phone_number': self.super.phone_number, 'password': self.password},
                                format='json')
        self.super_token = resp.data['access']

        self.user_moderator = Account.objects.create_user(phone_number='+77771231213', password=self.password)
        self.user_moderator.is_moderator = True
        self.user_moderator.is_active = True
        self.user_moderator.is_phone_confirmed = True
        self.user_moderator.save()
        resp = self.client.post(url, {'phone_number': self.user_moderator.phone_number, 'password': self.password},
                                format='json')
        self.user_moderator_token = resp.data['access']

        self.user_1 = Account.objects.create_user(phone_number='+77771231214', password=self.password)
        self.user_1.is_active = True
        self.user_1.is_phone_confirmed = True
        self.user_1.save()
        resp = self.client.post(url, {'phone_number': self.user_1.phone_number, 'password': self.password},
                                format='json')
        self.user_1_token = resp.data['access']

        self.user_2 = Account.objects.create_user(phone_number='+77771231215', password=self.password)
        self.user_2.is_active = True
        self.user_2.is_phone_confirmed = True
        self.user_2.save()
        resp = self.client.post(url, {'phone_number': self.user_2.phone_number, 'password': self.password},
                                format='json')
        self.user_2_token = resp.data['access']

        self.user_3 = Account.objects.create_user(phone_number='+77771231216', password=self.password)
        self.user_3.is_active = True
        self.user_3.is_phone_confirmed = False
        self.user_3.save()
        resp = self.client.post(url, {'phone_number': self.user_3.phone_number, 'password': self.password},
                                format='json')
        self.user_3_token = resp.data['access']

        self.user_4 = Account.objects.create_user(phone_number='+77771231217', password=self.password)
        self.user_4.is_active = True
        self.user_4.is_phone_confirmed = True
        self.user_4.save()
        resp = self.client.post(url, {'phone_number': self.user_4.phone_number, 'password': self.password},
                                format='json')
        self.user_4_token = resp.data['access']

        self.user_5 = Account.objects.create_user(phone_number='+77771231218', password=self.password)
        self.user_5.is_active = True
        self.user_5.is_phone_confirmed = True
        self.user_5.save()
        resp = self.client.post(url, {'phone_number': self.user_5.phone_number, 'password': self.password},
                                format='json')
        self.user_5_token = resp.data['access']

        self.user_6 = Account.objects.create_user(phone_number='+77771231219', password=self.password)
        self.user_6.is_active = True
        self.user_6.is_phone_confirmed = True
        self.user_6.save()
        resp = self.client.post(url, {'phone_number': self.user_6.phone_number, 'password': self.password},
                                format='json')
        self.user_6_token = resp.data['access']
        self.user_6_token_refresh = resp.data['refresh']

        self.user_7 = Account.objects.create_user(phone_number='+77771231220', password=self.password)
        self.user_7.is_active = True
        self.user_7.is_phone_confirmed = True
        self.user_7.save()
        resp = self.client.post(url, {'phone_number': self.user_7.phone_number, 'password': self.password},
                                format='json')
        self.user_7_token = resp.data['access']

        self.category_1 = Category.objects.create(name='test1')
        self.category_2 = Category.objects.create(name='test2')

        self.project_1 = Project.objects.create(description='test', account=self.user_1, is_personal=False,
                                                category=self.category_1)
        self.project_2 = Project.objects.create(description='test', account=self.user_1, is_personal=False,
                                                category=self.category_2)
        self.project_3 = Project.objects.create(description='test', account=self.user_1, is_personal=False)

        self.project_4 = Project.objects.create(description='test', account=self.user_4, is_personal=False)

        self.project_5 = Project.objects.create(description='test', account=self.user_4, is_personal=False)

        self.comment_1 = Comment.objects.create(account=self.user_1, project=self.project_1, content='comment_1')
        self.comment_2 = Comment.objects.create(account=self.user_2, project=self.project_1, content='comment_2')
        self.comment_3 = Comment.objects.create(account=self.user_4, project=self.project_2, content='comment_3')

    def tearDown(self):
        None

    def test_project_like_view(self):
        """
        path: projects/likedislike/<uuid:pk>/
        Добавление лайка (дизлайка) к проекту
        Для любого зарегистрированного пользователя с проверенным телефоном
        """

        data = {
            "vote_type": "0"
        }

        client = APIClient()
        url = reverse('projects:project_like_dislike', kwargs={'pk': self.project_1.id})

        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_3_token)

        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_4_token)

        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(self.project_1.likes_count, 0)
        self.assertEqual(self.project_1.dislikes_count, 0)
        self.assertEqual(self.project_1.rating, 0)

        data = {
            "vote_type": "1"
        }

        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['project_id'], self.project_1.id)
        self.assertEqual(resp.data['is_liked'], 1)
        self.assertEqual(resp.data['likes_count'], 1)
        self.assertEqual(resp.data['dislikes_count'], 0)
        self.assertEqual(resp.data['rating'], 1)

        self.project_1.refresh_from_db()
        self.assertEqual(self.project_1.likes_count, 1)
        self.assertEqual(self.project_1.dislikes_count, 0)
        self.assertEqual(self.project_1.rating, 1)

        url = reverse('projects:project_details', kwargs={'pk': self.project_1.id})
        resp = client.get(url, format='json')
        self.assertEqual(resp.data['is_liked'], 1)

        url = reverse('projects:project_like_dislike', kwargs={'pk': self.project_1.id})

        data = {
            "vote_type": "-1"
        }

        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['project_id'], self.project_1.id)
        self.assertEqual(resp.data['is_liked'], -1)
        self.assertEqual(resp.data['likes_count'], 0)
        self.assertEqual(resp.data['dislikes_count'], 1)
        self.assertEqual(resp.data['rating'], -1)

        self.project_1.refresh_from_db()
        self.assertEqual(self.project_1.likes_count, 0)
        self.assertEqual(self.project_1.dislikes_count, 1)
        self.assertEqual(self.project_1.rating, -1)

        url = reverse('projects:project_details', kwargs={'pk': self.project_1.id})
        resp = client.get(url, format='json')
        self.assertEqual(resp.data['is_liked'], -1)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        url = reverse('projects:project_details', kwargs={'pk': self.project_1.id})
        resp = client.get(url, format='json')
        self.assertEqual(resp.data['is_liked'], 0)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_4_token)
        url = reverse('projects:project_like_dislike', kwargs={'pk': self.project_1.id})
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['project_id'], self.project_1.id)
        self.assertEqual(resp.data['is_liked'], 0)
        self.assertEqual(resp.data['likes_count'], 0)
        self.assertEqual(resp.data['dislikes_count'], 0)
        self.assertEqual(resp.data['rating'], 0)

        self.project_1.refresh_from_db()
        self.assertEqual(self.project_1.likes_count, 0)
        self.assertEqual(self.project_1.dislikes_count, 0)
        self.assertEqual(self.project_1.rating, 0)

        data = {
            "vote_type": "1"
        }

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_2_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_3_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_4_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = {
            "vote_type": "-1"
        }

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_5_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.project_1.refresh_from_db()
        self.assertEqual(self.project_1.likes_count, 3)
        self.assertEqual(self.project_1.dislikes_count, 1)
        self.assertEqual(self.project_1.rating, 2)

        url = reverse('projects:project_like_dislike', kwargs={'pk': 'dd9fb68e-a1bf-4f58-9bdf-4dc8de8f62a7'})
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_5_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_like_view(self):
        """
        path: projects/comment/likedislike/<uuid:pk>/
        Добавление лайка (дизлайка) к комментарию
        Для любого зарегистрированного пользователя с проверенным телефоном
        """

        data = {
            "vote_type": "1"
        }

        client = APIClient()
        url = reverse('projects:project_comment_like_dislike', kwargs={'pk': self.comment_1.id})

        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_3_token)

        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_4_token)

        self.assertEqual(self.comment_1.likes_count, 0)
        self.assertEqual(self.comment_1.dislikes_count, 0)
        self.assertEqual(self.comment_1.rating, 0)

        data = {
            "vote_type": "-1"
        }

        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['comment_id'], self.comment_1.id)
        self.assertEqual(resp.data['is_liked'], -1)
        self.assertEqual(resp.data['likes_count'], 0)
        self.assertEqual(resp.data['dislikes_count'], 1)
        self.assertEqual(resp.data['rating'], -1)

        self.comment_1.refresh_from_db()
        self.assertEqual(self.comment_1.likes_count, 0)
        self.assertEqual(self.comment_1.dislikes_count, 1)
        self.assertEqual(self.comment_1.rating, -1)

        url = reverse('projects:project_comment_all_list', kwargs={'pk': self.project_1.id})
        resp = client.get(url, format='json')
        results = resp.data['results']
        comment = results[0]
        self.assertEqual(comment['is_liked'], -1)

        url = reverse('projects:project_comment_like_dislike', kwargs={'pk': self.comment_1.id})

        data = {
            "vote_type": "1"
        }

        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['comment_id'], self.comment_1.id)
        self.assertEqual(resp.data['is_liked'], 1)
        self.assertEqual(resp.data['likes_count'], 1)
        self.assertEqual(resp.data['dislikes_count'], 0)
        self.assertEqual(resp.data['rating'], 1)

        self.comment_1.refresh_from_db()
        self.assertEqual(self.comment_1.likes_count, 1)
        self.assertEqual(self.comment_1.dislikes_count, 0)
        self.assertEqual(self.comment_1.rating, 1)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        url = reverse('projects:project_comment_all_list', kwargs={'pk': self.project_1.id})
        resp = client.get(url, format='json')
        results = resp.data['results']
        comment = results[0]
        self.assertEqual(comment['is_liked'], 0)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_4_token)
        url = reverse('projects:project_comment_like_dislike', kwargs={'pk': self.comment_1.id})
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['comment_id'], self.comment_1.id)
        self.assertEqual(resp.data['is_liked'], 0)
        self.assertEqual(resp.data['likes_count'], 0)
        self.assertEqual(resp.data['dislikes_count'], 0)
        self.assertEqual(resp.data['rating'], 0)

        self.comment_1.refresh_from_db()
        self.assertEqual(self.comment_1.likes_count, 0)
        self.assertEqual(self.comment_1.dislikes_count, 0)
        self.assertEqual(self.comment_1.rating, 0)

        data = {
            "vote_type": "1"
        }

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_2_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_3_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_4_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = {
            "vote_type": "-1"
        }

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_5_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.comment_1.refresh_from_db()
        self.assertEqual(self.comment_1.likes_count, 3)
        self.assertEqual(self.comment_1.dislikes_count, 1)
        self.assertEqual(self.comment_1.rating, 2)

        url = reverse('projects:project_comment_like_dislike', kwargs={'pk': 'dd9fb68e-a1bf-4f58-9bdf-4dc8de8f62a7'})
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_5_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
