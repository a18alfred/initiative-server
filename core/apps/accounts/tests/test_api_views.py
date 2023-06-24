from core.apps.accounts.models import Account, PhoneCodeVerification
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


class AccountsViewsTestCase(APITestCase):
    """
    Тестирование Views
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

    def test_account_successful_registration(self):
        """
        path: /api/auth/users/
        Тестируем регистрацию пользователя успешно
        """
        client = APIClient()
        url = '/api/auth/users/'

        resp = self.client.post(url, {'phone_number': '+89521252512', 'password': self.password}, format='json')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue('data' in resp.data)
        data = resp.data['data']
        self.assertTrue('id' in data)
        self.assertTrue('refresh' in data)
        self.assertTrue('access' in data)

    def test_account_successful_registration(self):
        """
        path: /api/auth/users/
        Тестируем регистрацию пользователя неуспешно
        """
        client = APIClient()
        url = '/api/auth/users/'

        resp = self.client.post(url, {'phone_number': '+89', 'password': self.password}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = self.client.post(url, {'phone_number': '+89521252514', 'password': 'dfdsf'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_jwt_auth(self):
        """
        path: auth/login/
        Тестируем авторизацию пользователя с несуществующими данными
        """
        client = APIClient()
        url = reverse('accounts:account_login')

        resp = self.client.post(url, {'phone_number': '+89521231212', 'password': self.password}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('access' in resp.data)
        self.assertFalse('refresh' in resp.data)

    def test_successful_jwt_auth(self):
        """
        path: auth/login/
        Тестируем авторизацию пользователя и получение JWT токенов
        """
        client = APIClient()
        url = reverse('accounts:account_login')

        resp = self.client.post(url, {'phone_number': '+77771231212', 'password': self.password}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data)
        self.assertTrue('refresh' in resp.data)
        self.assertTrue('account' in resp.data)

        account = resp.data['account']

        self.assertEqual(account['id'], self.super.id)
        self.assertEqual(account['phone_number'], self.super.phone_number)
        self.assertEqual(account['is_active'], str(self.super.is_active))
        self.assertEqual(account['is_phone_confirmed'], str(self.super.is_phone_confirmed))
        self.assertEqual(account['is_superuser'], str(self.super.is_superuser))
        self.assertEqual(account['is_moderator'], str(self.super.is_moderator))
        self.assertTrue('profile' in account)

        profile = account['profile']

        self.assertEqual(profile['first_name'], self.super.account_profile.first_name)
        self.assertEqual(profile['middle_name'], self.super.account_profile.middle_name)
        self.assertEqual(profile['last_name'], self.super.account_profile.last_name)
        self.assertEqual(profile['email'], self.super.account_profile.email)

    def test_view_accounts_list_only_for_superuser(self):
        """
        path: accounts/all/
        Тестируем получение списка всех пользователей
        Список может получить только superuser
        Остальные пользователи получат 401 или 403 ошибку
        """

        url = reverse('accounts:accounts_list')
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + 'abc')
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_account_update_only_for_superuser(self):
        """
        path: accounts/update/<int:pk>/
        Тестируем обновление прав аккаунта. Только суперюзер имеет на это право.
        """

        data = {
            "is_moderator": True,
        }

        url = reverse('accounts:account_update', kwargs={'pk': self.user_moderator.id})
        resp = self.client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_moderator_token)
        resp = client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        resp = client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_account_delete_only_for_superuser_or_owner(self):
        """
        path: accounts/delete/<int:pk>/
        Тестируем удаление аккаунта. Только суперюзер и вдаделец акаунта имеет на это право.
        """

        url = reverse('accounts:account_delete', kwargs={'pk': self.user_4.id})
        resp = self.client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_5_token)
        resp = client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_moderator_token)
        resp = client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_4_token)
        resp = client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('accounts:account_delete', kwargs={'pk': self.user_5.id})
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        resp = client.delete(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_view_account_details_only_for_owner_or_superuser_or_moderator(self):
        """
        path: accounts/details/<int:pk>/
        Тестируем получение детального аккаунта.
        Может получить только владелец аккаунта(owner) или superuser или модератор
        Остальные пользователи получат 403 ошибку
        """
        url = reverse('accounts:account_details', kwargs={'pk': self.user_1.id})
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + 'abc')
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_2_token)
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('accounts:account_details', kwargs={'pk': '24ff0a1d-b38e-472c-9ee5-35a5b396ce21'})
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_profile_update_only_for_owner_or_superuser(self):
        """
        path: profile/update/<uuid:pk>/
        Тестируем внесение изменений профайла.
        Может произвести только владелец аккаунта(owner) или superuser
        Остальные пользователи получат 403 ошибку
        """
        client = APIClient()
        data = {
            "first_name": "test",
        }
        url = reverse('accounts:profile_update', kwargs={'pk': self.user_1.id})

        resp = self.client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + 'abc')
        resp = client.put(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        resp = client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_2_token)
        resp = client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('accounts:profile_update', kwargs={'pk': '24ff0a1d-b38e-472c-9ee5-35a5b396ce21'})
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        resp = client.put(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_code_request(self):
        """
        path: auth/phone/getcode/<uuid:pk>/
        Тестируем запрос на получения кода проверки номера телефона
        Слишком частый запрос возвращает 400 ошибку
        """
        client = APIClient()
        url = reverse('accounts:account_request_phone_code', kwargs={'pk': self.user_1.id})

        resp = self.client.post(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_2_token)
        resp = client.post(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.post(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_1_token)
        resp = client.post(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('accounts:account_request_phone_code', kwargs={'pk': '24ff0a1d-b38e-472c-9ee5-35a5b396ce21'})
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        resp = client.post(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_code_verify(self):
        """
        path: auth/phone/verify/<uuid:pk>/
        Тестируем запрос на получения кода проверки номера телефона
        Слишком частый запрос возвращает 400 ошибку
        """
        client = APIClient()
        url = reverse('accounts:account_request_phone_code', kwargs={'pk': self.user_3.id})
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_3_token)
        resp = client.post(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = {
            "code": "0",
        }
        url = reverse('accounts:account_verify_phone_code', kwargs={'pk': self.user_3.id})

        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_2_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_3_token)
        resp = client.post(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_3_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "code": PhoneCodeVerification.objects.get(account=self.user_3).code,
        }
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_3_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_3_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.user_3_token)
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('accounts:account_verify_phone_code', kwargs={'pk': '24ff0a1d-b38e-472c-9ee5-35a5b396ce21'})
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        resp = client.post(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_code_request_password_reset(self):
        """
        path: auth/phone/getcode/password-reset/
        Тестируем запрос на получения кода для смены пароля
        Слишком частый запрос возвращает 400 ошибку
        """
        url = reverse('accounts:account_request_phone_code_password_reset')

        resp = self.client.post(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "phone_number": "+78951",
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        data = {
            "phone_number": self.user_2.phone_number,
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_code_verify_password_reset(self):
        """
        path: auth/phone/verify/password-reset/
        Тестируем проверку телефонного кода для сброса пароля
        Слишком частый запрос возвращает 400 ошибку
        """
        url = reverse('accounts:account_verify_phone_code_password_reset')

        resp = self.client.post(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "phone_number": "+78951",
            "code": "0"
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse('accounts:account_request_phone_code_password_reset')
        data = {
            "phone_number": self.user_7.phone_number,
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        url = reverse('accounts:account_verify_phone_code_password_reset')
        data = {
            "phone_number": self.user_7.phone_number,
            "code": "0"
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "phone_number": self.user_7.phone_number,
            "code": PhoneCodeVerification.objects.get(account=self.user_7).code
        }

        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertTrue('uid' in resp.data)
        self.assertTrue('token' in resp.data)

        new_pass = "Regfgdf#fgg1"
        url = '/api/auth/users/reset_password_confirm/'
        data = {
            "uid": resp.data['uid'],
            "token": resp.data['token'],
            "new_password": new_pass,
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_blacklist_token_view(self):
        """
        path: auth/logout/
        Тестируем внесение в черный список refresh token.
        """

        data = {
            "refresh": self.user_6_token_refresh
        }

        client = APIClient()

        url = reverse('accounts:account_logout')

        client.credentials(HTTP_AUTHORIZATION='')
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_205_RESET_CONTENT)

        client.credentials(HTTP_AUTHORIZATION='')
        resp = client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
