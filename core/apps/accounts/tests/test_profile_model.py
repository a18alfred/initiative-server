from django.test import TestCase
from core.apps.accounts.models import Account, Profile


class ProfileModelTestCase(TestCase):
    """
    Тестируем модель Profile
    """

    def test_account_str_return(self):
        """
        Тестируем __str__ модели PhoneCodeVerification
        :return: phone_number
        """
        phone_number = '+79827965529'
        password = 'asdasdl2@asAS'
        user = Account.objects.create_user(phone_number=phone_number, password=password)
        self.assertEqual(Profile.objects.get(account_id=user.id).__str__(), phone_number)
