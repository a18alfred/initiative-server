from django.test import TestCase
from core.apps.accounts.models import Account


class AccountModelTestCase(TestCase):
    """
    Тестируем модель Account
    """

    def test_account_str_return(self):
        """
        Тестируем __str__ модели Account
        :return: phone_number
        """
        phone_number = '+79827965529'
        password = 'asdasdl2@asAS'
        user = Account.objects.create_user(phone_number=phone_number, password=password)
        self.assertEqual(user.__str__(), phone_number)
