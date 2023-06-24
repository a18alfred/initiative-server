from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from .validators import phone_number_regex
from core.settings import NUMBER_OF_PHONE_CODE_DIGITS, MAX_CODE_NUMBER, CODE_ACTIVE_IN_MINUTES
from django.utils import timezone
import random
import uuid


class Account(AbstractUser):
    """
    Кастомная user модель для аккаунтов.
    username отсутсвует
    phone_number является логином

    phone_number - телефон пользователя
    is_phone_confirmed - подтвердён или нет телефон
    is_moderator - флажок является ли пользователь модератором
    is_banned - флажок забанен ли пользователь
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    username = None
    email = None

    phone_number = models.CharField(validators=[phone_number_regex],
                                    max_length=16,
                                    unique=True,
                                    editable=False,
                                    verbose_name="телефон")

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    is_phone_confirmed = models.BooleanField(default=False, verbose_name="телефон подтверждён")
    is_moderator = models.BooleanField(default=False, verbose_name="модератор")

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

    class Meta:
        ordering = ['date_joined']
        verbose_name = "аккаунт"
        verbose_name_plural = "аккаунты"


class Profile(models.Model):
    """
       Модель для хранения пользовательских данных.
       account - аккаунт к которому привязан профайл
       first_name - имя
       middle_name - отчество
       last_name - фамилия
       email - email
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="account_profile")

    first_name = models.CharField(max_length=100, blank=True, verbose_name="имя")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="отчество")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="фамилия")

    email = models.EmailField(blank=True, verbose_name="электронная почта")

    def __str__(self):
        return self.account.phone_number

    class Meta:
        verbose_name = "профиль пользователя"
        verbose_name_plural = "профили пользователей"


class PhoneCodeVerification(models.Model):
    """
       Модель для хранения последнего отправленного кода на телефон.
       account - аккаунт к которому привязан профайл
       code - сгенерированный год верификации
       created_at - время генерации кода
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="account_phone_code_verification")

    code = models.CharField(blank=True, null=True, max_length=6, verbose_name='код отправленный на телефон')

    checked_number = models.IntegerField(default=0, verbose_name='Количество проверок')

    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата генерации кода')

    def generate_code(self):
        if timezone.now() < (self.created_at + CODE_ACTIVE_IN_MINUTES) and self.code is not None:
            return False
        temp_code = str(random.randint(0, MAX_CODE_NUMBER))
        self.code = temp_code.zfill(NUMBER_OF_PHONE_CODE_DIGITS)[-NUMBER_OF_PHONE_CODE_DIGITS:]
        self.checked_number = 0
        self.created_at = timezone.now()
        self.save()
        return True

    def verify_code(self, user_code):
        if self.code is None:
            return False

        if timezone.now() > (self.created_at + CODE_ACTIVE_IN_MINUTES):
            return False

        checked_number = self.checked_number + 1
        if checked_number > 3:
            return False

        self.checked_number = checked_number
        self.save()

        if self.code == user_code:
            self.account.is_phone_confirmed = True
            self.account.save()
            return True

        return False

    def __str__(self):
        return self.account.phone_number

    class Meta:
        verbose_name = "код подтверждения"
        verbose_name_plural = "коды подтверждения"
