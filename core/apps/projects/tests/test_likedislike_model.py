from django.db.transaction import TransactionManagementError
from django.test import TestCase
from core.apps.projects.models import LikeDislike, Project
from core.apps.accounts.models import Account
from django.contrib.contenttypes.models import ContentType


class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.password = 'asdasdl2@asAS'
        self.super = Account.objects.create_superuser(phone_number='+77771231212', password=self.password)
        self.super.account_profile.first_name = 'first_name'
        self.super.account_profile.middle_name = 'middle_name'
        self.super.account_profile.last_name = 'last_name'
        self.super.account_profile.email = 'email'

        self.user_1 = Account.objects.create_user(phone_number='+77771231214', password=self.password)
        self.user_1.is_active = True
        self.user_1.is_phone_confirmed = True
        self.user_1.save()

        self.project_1 = Project.objects.create(description='test', account=self.super, is_personal=False)

    def tearDown(self):
        self.super.delete()
        self.user_1.delete()
        self.project_1.delete()

    def test_likedislike_model_save_auto_count(self):
        """
        Тестируем автоматический подсчёт лайков у объекта
        """
        self.assertEqual(self.project_1.likes_count, 0)
        self.assertEqual(self.project_1.dislikes_count, 0)
        self.assertEqual(self.project_1.rating, 0)

        self.project_1.votes.create(account=self.super, vote=1)
        self.project_1.votes.create(account=self.user_1, vote=-1)

        self.project_1.refresh_from_db()

        self.assertEqual(self.project_1.votes.likes().count(), 1)
        self.assertEqual(self.project_1.votes.dislikes().count(), 1)
        self.assertEqual(self.project_1.votes.sum_rating(), 0)

        self.assertEqual(self.project_1.likes_count, 1)
        self.assertEqual(self.project_1.dislikes_count, 1)
        self.assertEqual(self.project_1.rating, 0)
