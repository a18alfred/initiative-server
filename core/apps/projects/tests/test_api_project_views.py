from core.apps.accounts.models import Account
from core.apps.projects.models import Category, Project
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from core.service import create_test_image
from django.conf import settings


class ProjectAPIViewsTestCase(APITestCase):
    """
    Тестирование Views API Project
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

    def test_project_details_view(self):
        """
        path: projects/details/<uuid:pk>/
        Получение детальной информации о проекте
        """

        url = reverse('projects:project_details', kwargs={'pk': self.project_1.id})
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['description'], self.project_1.description)

        resp = self.client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        url = reverse('projects:project_details', kwargs={'pk': '24ff0a1d-b38e-472c-9ee5-35a5b396ce21'})
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_project_create_no_links_no_attachments(self):
        """
        path: projects/create/
        Создание проекта
        Для любого зарегистрированного пользователя с проверенным телефоном
        """

        data = {
            "description": "description",
            "is_personal": True
        }
        client = APIClient()
        url = reverse('projects:project_create')

        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_3_token)

        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        data = {
            "description": "",
            "is_personal": True
        }
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_4_token)

        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "description": "description",
            "is_personal": True
        }

        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_project_create_with_links_with_attachments(self):
        """
        path: projects/create/
        Создание проекта с ссылки и файлами
        Для любого зарегистрированного пользователя с проверенным телефоном
        """

        data = {
            "description": "description",
            "is_personal": True,
            "uploaded_files": create_test_image()
        }
        client = APIClient()
        url = reverse('projects:project_create')

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_4_token)

        resp = client.post(url, data, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data['attachments']), 1)

        data = {
            "description": "description",
            "is_personal": True,
            "uploaded_files": [create_test_image(), create_test_image()],
        }

        resp = client.post(url, data, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data['attachments']), 2)

        data = {
            "description": "description",
            "is_personal": True,
            "uploaded_files": [create_test_image(), create_test_image(), create_test_image()],
        }

        resp = client.post(url, data, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data['attachments']), 2)

        link_not_valid = 'admin'
        link = 'http://127.0.0.1:8000/admin/'

        data = {
            "description": "description",
            "is_personal": True,
            "uploaded_links": link_not_valid,
        }

        resp = client.post(url, data, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "description": "description",
            "is_personal": True,
            "uploaded_links": link,
        }

        resp = client.post(url, data, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data['links']), 1)

        data = {
            "description": "description",
            "is_personal": True,
            "uploaded_links": [link, link],
            "uploaded_files": [create_test_image(), create_test_image()],
        }

        resp = client.post(url, data, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data['links']), 2)
        self.assertEqual(len(resp.data['attachments']), 2)

    def test_project_delete(self):
        """
        path: projects/delete/<uuid:pk>/
        Удаление проекта
        403 - если не создатель проекта, не модератор или не суперюзер
        """
        client = APIClient()
        url = reverse('projects:project_delete', kwargs={'pk': self.project_4.id})

        resp = client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_2_token)
        resp = client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_4_token)
        resp = client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('projects:project_delete', kwargs={'pk': self.project_5.id})
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_moderator_token)
        resp = client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('projects:project_delete', kwargs={'pk': self.project_5.id})
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_moderator_token)
        resp = client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_project_update(self):
        """
        path: projects/update/<uuid:pk>/
        Внесение изменений в проект
        403 - если не создатель проекта, не модератор или не суперюзер
        """
        client = APIClient()
        url = reverse('projects:project_update', kwargs={'pk': self.project_1.id})

        data = {
            "description": "description_updated",
            "is_approved": True
        }
        resp = client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_2_token)
        resp = client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        resp = client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.project_1.refresh_from_db()
        self.assertEqual(self.project_1.is_approved, False)
        self.assertEqual(resp.data['description'], 'description_updated')

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_moderator_token)
        resp = client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        resp = client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_project_super_update(self):
        """
        path: projects/updatesuper/<uuid:pk>/
        Внесение изменений в проект модератором или супером
        """
        client = APIClient()
        url = reverse('projects:project_super_update', kwargs={'pk': self.project_1.id})

        data = {
            "is_approved": True
        }
        resp = client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_2_token)
        resp = client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_moderator_token)
        resp = client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        resp = client.patch(url, data, format='json')
        self.project_1.refresh_from_db()
        self.assertEqual(self.project_1.is_approved, True)
        self.assertEqual(resp.data['is_approved'], True)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        resp = client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_project_user_created_list(self):
        """
        path: projects/mylist/
        Получение списка всех проектов созданных пользователем
        """

        client = APIClient()
        url = reverse('projects:project_user_created_list')

        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_7_token)
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data['results']), 0)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data['results']), 3)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_3_token)
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_all_approved_list(self):
        """
        path: projects/approved/
        Получение списка всех опубликованных проектов
        """

        client = APIClient()
        url = reverse('projects:project_all_approved_list')

        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data['results']), 0)

        self.project_1.is_approved = True
        self.project_1.save()
        self.project_2.is_approved = True
        self.project_2.save()
        resp = client.get(url, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data['results']), 2)

    def test_project_all_list(self):
        """
        path: projects/approved/
        Получение списка всех проектов
        Только для модераторов и суперов
        """

        client = APIClient()
        url = reverse('projects:project_all_list')

        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_moderator_token)
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data['results']), 5)
