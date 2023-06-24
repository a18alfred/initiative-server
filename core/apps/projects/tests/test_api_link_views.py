from core.apps.accounts.models import Account
from core.apps.projects.models import Category, Project, Link
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.conf import settings


class LinkAPIViewsTestCase(APITestCase):
    """
    Тестирование Views API Link
    """

    def setUp(self):
        """
        Создаём пользователей с разными правами:
        СуперЮзер
        Модератор
        Обычный пользователь
        Обычный пользователь
        """
        settings.MAX_NUMBER_OF_ATTACHMENTS_PER_PROJECT = 2
        settings.MAX_NUMBER_OF_LINKS_PER_PROJECT = 2

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

        self.link_1 = Link.objects.create(project=self.project_5, url='http://127.0.0.1:8000/')

    def tearDown(self):
        self.super.delete()
        self.user_moderator.delete()
        self.user_1.delete()
        self.user_2.delete()
        self.user_3.delete()
        self.user_4.delete()
        self.user_5.delete()
        self.user_6.delete()
        self.user_7.delete()
        self.category_1.delete()
        self.category_2.delete()
        self.project_1.delete()
        self.project_2.delete()
        self.project_3.delete()
        self.project_4.delete()
        self.project_5.delete()
        self.link_1.delete()

    def test_link_add_new(self):
        """
        path: projects/link/add/'
        Добавление новой ссылке к проекту
        Только для модераторов и суперов и владельцев проекта
        """

        client = APIClient()
        url = reverse('projects:project_link_add')

        data = {
            "url": 'http://127.0.0.1:8000/'
        }

        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "project": str(self.project_1.id),
            "url": 'http'
        }

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "project": str(self.project_1.id),
            "url": 'http://127.0.0.1:8000/'
        }

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_2_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_moderator_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_link_update_new(self):
        """
        path: projects/link/update/<uuid:pk>/
        Тестируем удаление и изменение ссылок проекта
        """

        client = APIClient()
        url = reverse('projects:project_link_update_delete',
                      kwargs={'pk': self.link_1.id})

        data = {
            "url": "http://127.0.0.1/",
        }

        resp = client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_4_token)
        resp = client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        resp = client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_moderator_token)
        resp = client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_4_token)
        resp = client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
