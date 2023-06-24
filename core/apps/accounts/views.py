from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from django_filters import rest_framework as filters
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .service import AccountFilter
from .permissions import IsOwner, IsOwnerOrSuperUser, IsSuperUser, IsOwnerOrSuperUserOrModerator, IsPhoneConfirmed, \
    IsAccountOwnerOrSuperUser, IsAccountOwnerOrSuperUserOrModerator
from .models import Account, Profile, PhoneCodeVerification
from .serializers import AccountSerializer, AccountUpdateSerializer, ProfileSerializer, MyTokenObtainPairSerializer
from django.http import Http404
from django.contrib.auth.tokens import default_token_generator
from djoser import utils


class AccountListView(ListAPIView):
    """
    Класс для получения списка аккаунтов с возможностью фильрации.
    Только для СуперЮзера
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsSuperUser, ]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AccountFilter


class AccountUpdateView(UpdateAPIView):
    """
    Класс для внесения изменения в определённый аккаунт. Например права пользователя.
    Только для СуперЮзера.
    """
    queryset = Account.objects.all()
    serializer_class = AccountUpdateSerializer
    permission_classes = [IsSuperUser, ]


class AccountDetailView(RetrieveAPIView):
    """
    Класс для получения профайла пользователя.
    Только для владельца профайла и СуперЮзера
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAccountOwnerOrSuperUserOrModerator, ]


class AccountDeleteView(DestroyAPIView):
    """
    Класс для удаления аккаунта.
    Только для СуперЮзера
    """
    queryset = Account.objects.all()
    serializer_class = AccountUpdateSerializer
    permission_classes = [IsAccountOwnerOrSuperUser, ]


class ProfileUpdateView(UpdateAPIView):
    """
    Класс для внесения изменений в профайл пользователя.
    Только для владельца профайла и СуперЮзера
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrSuperUser, IsPhoneConfirmed]

    def get_object(self):
        pk = self.kwargs['pk']
        try:
            obj = Profile.objects.get(account_id=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Profile.DoesNotExist:
            raise Http404


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class BlacklistTokenUpdateView(APIView):
    """
    Используется для разлогинивания. Действующий refresh токен вносится в черный список.
    """
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CodeRequestView(APIView):
    """
    Класс для запроса кода для верификации телефона
    """
    permission_classes = [IsOwner]

    def get_object(self):
        pk = self.kwargs['pk']
        try:
            obj = PhoneCodeVerification.objects.get(account_id=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except PhoneCodeVerification.DoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.generate_code():
            return Response(
                {"detail": "Код успешно отправлен"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Слишком частый запрос"}, status=status.HTTP_400_BAD_REQUEST
            )


class CodeVerifyView(APIView):
    """
    Класс для проверки кода с телефона
    """
    permission_classes = [IsOwner]

    def get_object(self):
        pk = self.kwargs['pk']
        try:
            obj = PhoneCodeVerification.objects.get(account_id=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except PhoneCodeVerification.DoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            code = request.data["code"]
            if obj.verify_code(code):
                return Response(
                    {"detail": "Телефон подтверждён"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "Неверный код или время кода истекло"}, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"detail": "Поле code обязательно"}, status=status.HTTP_400_BAD_REQUEST
            )


class CodeRequestPasswordResetView(APIView):
    """
    Класс для запроса кода для смены забытого пароля
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            phone_number = request.data["phone_number"]
            obj = PhoneCodeVerification.objects.get(account__phone_number=phone_number)

            if obj.generate_code():
                return Response(
                    {"detail": "Код успешно отправлен"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "Слишком частый запрос"}, status=status.HTTP_400_BAD_REQUEST
                )
        except PhoneCodeVerification.DoesNotExist:
            raise Http404
        except Exception as e:
            return Response(
                {"detail": "Поле phone_number обязательно"}, status=status.HTTP_400_BAD_REQUEST
            )


class CodeVerifyPasswordResetView(APIView):
    """
    Класс для проверки кода с телефона для смены забытого пароля
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            phone_number = request.data["phone_number"]
            obj = PhoneCodeVerification.objects.get(account__phone_number=phone_number)

            code = request.data["code"]
            if obj.verify_code(code):
                context = {"uid": utils.encode_uid(obj.account.pk),
                           "token": default_token_generator.make_token(obj.account)}
                return Response(
                    context, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "Неверный код или время кода истекло"}, status=status.HTTP_400_BAD_REQUEST
                )
        except PhoneCodeVerification.DoesNotExist:
            raise Http404
        except Exception as e:
            return Response(
                {"detail": "Поле phone_number и code обязательно"}, status=status.HTTP_400_BAD_REQUEST
            )
