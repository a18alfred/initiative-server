# Generated by Django 4.0.6 on 2022-08-09 15:23

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('phone_number', models.CharField(editable=False, max_length=16, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='телефон')),
                ('is_phone_confirmed', models.BooleanField(default=False, verbose_name='телефон подтверждён')),
                ('is_moderator', models.BooleanField(default=False, verbose_name='модератор')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'аккаунт',
                'verbose_name_plural': 'аккаунты',
                'ordering': ['date_joined'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=100, verbose_name='имя')),
                ('middle_name', models.CharField(blank=True, max_length=100, verbose_name='отчество')),
                ('last_name', models.CharField(blank=True, max_length=100, verbose_name='фамилия')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='электронная почта')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'профиль пользователя',
                'verbose_name_plural': 'профили пользователей',
            },
        ),
        migrations.CreateModel(
            name='PhoneCodeVerification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('code', models.CharField(blank=True, max_length=6, null=True, verbose_name='код отправленный на телефон')),
                ('checked_number', models.IntegerField(default=0, verbose_name='Количество проверок')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата генерации кода')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account_phone_code_verification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'код подтверждения',
                'verbose_name_plural': 'коды подтверждения',
            },
        ),
    ]
