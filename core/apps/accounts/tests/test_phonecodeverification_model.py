from django.test import TestCase
from core.apps.accounts.models import Account, PhoneCodeVerification
from freezegun import freeze_time


class PhoneCodeVerificationModelTestCase(TestCase):
    """
    Тестируем модель PhoneCodeVerification
    """

    @freeze_time("2022-01-14 12:00:01")
    def setUp(self):
        self.phone_number = '+79827965529'
        self.password = 'asdasdl2@asAS'
        self.user = Account.objects.create_user(phone_number=self.phone_number, password=self.password)
        self.phv = PhoneCodeVerification.objects.get(account_id=self.user.id)

    def test_modal_str_return(self):
        """
        Тестируем __str__ модели PhoneCodeVerification
        :return: phone_number
        """
        self.assertEqual(PhoneCodeVerification.objects.get(account_id=self.user.id).__str__(), self.phone_number)

    def test_generate_code_return(self):
        """
        Тестируем метод generate_code
        :return: True - если успешно код сгенерирован
                 False - если запрос был слишком ранним после последнего запроса
        """
        freezer = freeze_time("2022-01-15 12:00:00")
        freezer.start()
        self.assertEqual(self.phv.generate_code(), True)
        self.assertEqual(self.phv.generate_code(), False)
        self.assertEqual(self.phv.verify_code('0'), False)
        self.assertEqual(self.phv.checked_number, 1)
        freezer.stop()

        freezer = freeze_time("2022-01-15 12:06:00")
        freezer.start()
        self.assertEqual(self.phv.generate_code(), True)
        self.assertEqual(self.phv.checked_number, 0)
        freezer.stop()

    def test_verify_code_return(self):
        """
        Тестируем метод verify_code
        :return: True - если код верный
                 False - если время действия кода истекло или слишком много запросов (более 3 раз)
        """
        freezer = freeze_time("2022-01-15 12:00:00")
        freezer.start()
        self.assertEqual(self.phv.generate_code(), True)
        self.assertEqual(self.phv.verify_code('0'), False)
        self.assertEqual(self.phv.verify_code('0'), False)
        self.assertEqual(self.phv.verify_code('0'), False)
        self.assertEqual(self.phv.verify_code('0'), False)
        self.assertEqual(self.phv.checked_number, 3)
        freezer.stop()

        freezer = freeze_time("2022-01-15 12:06:00")
        freezer.start()
        self.assertEqual(self.phv.generate_code(), True)
        self.assertEqual(self.phv.verify_code(self.phv.code), True)
        self.assertEqual(self.phv.verify_code(self.phv.code), True)
        self.assertEqual(self.phv.verify_code(self.phv.code), True)
        self.assertEqual(self.phv.verify_code(self.phv.code), False)
        freezer.stop()

        freezer = freeze_time("2022-01-15 12:20:00")
        freezer.start()
        self.assertEqual(self.phv.generate_code(), True)
        self.assertEqual(self.phv.verify_code(self.phv.code), True)
        freezer.stop()

        freezer = freeze_time("2022-01-15 12:40:00")
        freezer.start()
        self.assertEqual(self.phv.verify_code(self.phv.code), False)
        freezer.stop()
