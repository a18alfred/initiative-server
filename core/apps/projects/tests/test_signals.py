from core.apps.accounts.models import Account
from core.apps.projects.models import Category, Project, Attachment
from django.urls import reverse
from rest_framework.test import APITestCase
from core.service import create_test_image
from django.conf import settings
import os
from core.apps.projects.signals import auto_delete_file_on_change_attachment, auto_delete_icon_on_change, \
    auto_delete_icon_on_delete


class ProjectSignalsTestCase(APITestCase):
    """
    Тестирование Signals
    """

    def setUp(self):
        """
        Создаём пользователей с разными правами:
        СуперЮзер
        Модератор
        Обычный пользователь
        Обычный пользователь
        """
        settings.MAX_NUMBER_OF_ATTACHMENTS_PER_PROJECT = 5
        settings.MAX_NUMBER_OF_LINKS_PER_PROJECT = 5

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

        self.attachment_1 = Attachment.objects.create(project=self.project_5, uploaded_file=create_test_image())
        self.attachment_2 = Attachment.objects.create(project=self.project_5, uploaded_file=create_test_image())

    def tearDown(self):
        None

    def test_auto_delete_file_on_change(self):
        """
        Тестируем удаление старого файла фото после обновления фото и удаление директории
        если файлов в ней нет.
        """

        dir_name_project = '/'.join([str(settings.MEDIA_ROOT), 'projects', str(self.project_5.id)])
        dir_name = '/'.join([str(settings.MEDIA_ROOT), 'projects', str(self.project_5.id), 'attachments', ])
        self.assertEqual(len(os.listdir(dir_name)), 2)

        self.attachment_1.uploaded_file = ''
        self.attachment_1.save()
        self.assertTrue(os.path.exists(dir_name))
        self.attachment_2.uploaded_file = ''
        self.attachment_2.save()
        self.assertFalse(os.path.exists(dir_name))

        self.attachment_1 = Attachment.objects.create(project=self.project_5, uploaded_file=create_test_image())
        self.attachment_1.save()
        self.assertTrue(os.path.exists(dir_name_project))
        self.project_5.delete()
        self.assertFalse(os.path.exists(dir_name_project))

        self.assertFalse(auto_delete_file_on_change_attachment(Attachment, self.attachment_1))

    def test_auto_delete_icon_on_delete(self):
        """
        Тестируем файла/фото из дериктории после удаления файла из модели категория
        """
        category1 = Category.objects.create(name='some test category1', icon=create_test_image())
        category2 = Category.objects.create(name='some test category2')
        dir_name1 = '/'.join([str(settings.MEDIA_ROOT), 'categories', str(category1.slug)])
        dir_name2 = '/'.join([str(settings.MEDIA_ROOT), 'categories', str(category2.slug)])
        dir_name_default = '/'.join([str(settings.MEDIA_ROOT), 'categories', 'default_category_icon.png'])

        self.assertEqual(len(os.listdir(dir_name1)), 1)
        self.assertFalse(os.path.exists(dir_name2))

        category1.delete()
        self.assertFalse(os.path.exists(dir_name1))
        category2.delete()
        self.assertTrue(os.path.exists(dir_name_default))

    def test_auto_delete_icon_on_change(self):
        category = Category.objects.create(name='test_category_test')
        category.id = None
        self.assertFalse(auto_delete_icon_on_change(Category, category))
