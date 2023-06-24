from rest_framework import serializers
from .models import Account, Profile
from .validators import phone_number_regex
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from djoser.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        profile = self.user.account_profile
        data['account'] = {
            'id': self.user.id,
            'phone_number': str(self.user.phone_number),
            'is_phone_confirmed': str(self.user.is_phone_confirmed),
            'is_active': str(self.user.is_active),
            'is_superuser': str(self.user.is_superuser),
            'is_moderator': str(self.user.is_moderator),
            'profile': {
                'first_name': str(profile.first_name),
                'middle_name': str(profile.middle_name),
                'last_name': str(profile.last_name),
                'email': str(profile.email),
            }
        }

        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'middle_name', 'last_name', 'email')


class ProfileShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'middle_name', 'last_name')


class AccountSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True, source='account_profile')

    class Meta:
        model = Account
        fields = ('id', 'phone_number', 'is_phone_confirmed', 'is_active', 'is_superuser', 'is_moderator', 'profile')


class AccountWithoutProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'phone_number', 'is_phone_confirmed', 'is_active', 'is_superuser', 'is_moderator')


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('is_active', 'is_moderator')


class AccountCommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True, source='account_profile')

    class Meta:
        model = Account
        fields = ('id', 'is_active', 'is_moderator', 'profile')


class AccountShortSerializer(serializers.ModelSerializer):
    profile = ProfileShortSerializer(read_only=True, source='account_profile')

    class Meta:
        model = Account
        fields = ('id', 'profile')


class CustomUserCreateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True, max_length=16, validators=[phone_number_regex])
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "password",
        )

    def to_representation(self, instance):
        data = super(CustomUserCreateSerializer, self).to_representation(instance)
        user_tokens = RefreshToken.for_user(instance)
        tokens = {'refresh': str(user_tokens), 'access': str(user_tokens.access_token)}
        data = {
            "data": data | tokens
        }
        return data

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user
