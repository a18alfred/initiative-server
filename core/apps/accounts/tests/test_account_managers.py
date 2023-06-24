from django.test import TestCase
from core.apps.accounts.managers import CustomUserManager
from core.apps.accounts.models import Account


class CustomUserManagerTestCase(TestCase):
    """
    Тестируем CustomUserManager
    """

    def test_create_user(self):
        """
        Создание обычного пользователя
        """
        phone_number = '+79827965525'
        password = 'asdasdl2@asAS'
        user = Account.objects.create_user(phone_number=phone_number, password=password)
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.is_phone_confirmed, False)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_moderator, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        self.assertTrue(user.has_usable_password())

    def test_create_user_without_phone_number(self):
        """
        Создание обычного пользователя без phone_number. Должны получить ошибку.
        """
        phone_number = ''
        password = 'asdasdl2@asAS'
        with self.assertRaisesMessage(ValueError, 'Телефонный номер обязателен'):
            user = Account.objects.create_user(phone_number=phone_number, password=password)

    def test_create_user_is_staff(self):
        phone_number = '+79827965526'
        password = 'asdasdl2@asAS'
        user = Account.objects.create_user(phone_number, password, is_staff=True)
        self.assertEqual(user.phone_number, phone_number)
        self.assertTrue(user.is_staff)

    def test_create_super_user_raises_error_on_false_is_superuser(self):
        with self.assertRaisesMessage(ValueError, 'Superuser должен иметь is_superuser = True.'):
            Account.objects.create_superuser(phone_number='+79827965528', password='test', is_superuser=False)

    def test_create_super_user_raises_error_on_false_is_stuff(self):
        with self.assertRaisesMessage(ValueError, 'Superuser должен иметь is_staff = True.'):
            Account.objects.create_superuser(phone_number='+79827965528', password='test', is_staff=False)

    def test_create_superuser_must_be_true_is_staff_is_superuser_is_active_is_moderator_is_phone_confirmed(
            self):
        """
        Тестируем создание superuser со всеми правами.
        """
        phone_number = '+79827965550'
        password = 'asdasdl2@asAS'
        user = Account.objects.create_superuser(phone_number, password)
        self.assertEqual(user.phone_number, phone_number)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_moderator)
        self.assertTrue(user.is_phone_confirmed)

    def test_make_random_password(self):
        allowed_chars = 'abcdef4@#gAATG'
        password = CustomUserManager().make_random_password(9, allowed_chars)
        self.assertEqual(len(password), 9)
        for char in password:
            self.assertIn(char, allowed_chars)
