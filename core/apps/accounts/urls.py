from django.urls import include, path
from .views import BlacklistTokenUpdateView, CodeRequestView, CodeVerifyView, CodeRequestPasswordResetView, \
    CodeVerifyPasswordResetView, AccountListView, AccountUpdateView, AccountDeleteView, \
    ProfileUpdateView, AccountDetailView, MyTokenObtainPairView

app_name = 'accounts'

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/login/', MyTokenObtainPairView.as_view(),
         name='account_login'),
    path('auth/logout/', BlacklistTokenUpdateView.as_view(),
         name='account_logout'),
    path('auth/phone/getcode/<uuid:pk>/', CodeRequestView.as_view(), name='account_request_phone_code'),
    path('auth/phone/verify/<uuid:pk>/', CodeVerifyView.as_view(), name='account_verify_phone_code'),
    path('auth/phone/getcode/password-reset/', CodeRequestPasswordResetView.as_view(),
         name='account_request_phone_code_password_reset'),
    path('auth/phone/verify/password-reset/', CodeVerifyPasswordResetView.as_view(),
         name='account_verify_phone_code_password_reset'),
    path('accounts/all/', AccountListView.as_view(), name='accounts_list'),
    path('accounts/update/<uuid:pk>/', AccountUpdateView.as_view(), name='account_update'),
    path('accounts/delete/<uuid:pk>/', AccountDeleteView.as_view(), name='account_delete'),
    path('accounts/details/<uuid:pk>/', AccountDetailView.as_view(), name='account_details'),
    path('profile/update/<uuid:pk>/', ProfileUpdateView.as_view(), name='profile_update'),
]
