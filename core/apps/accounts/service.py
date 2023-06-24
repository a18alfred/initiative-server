from django_filters import rest_framework as filters
from .models import Account, Profile


class ProfileFilter(filters.FilterSet):
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='contains')
    email = filters.CharFilter(field_name='email', lookup_expr='contains')

    class Meta:
        model = Profile
        fields = ['last_name', 'email']


class AccountFilter(filters.FilterSet):
    """
    Фильтр для работы со списком акаунтов
    """

    phone_number = filters.CharFilter(field_name='phone_number', lookup_expr='contains')
    is_active = filters.BooleanFilter(field_name='is_active')
    is_superuser = filters.BooleanFilter(field_name='is_superuser')
    is_moderator = filters.BooleanFilter(field_name='is_moderator')
    date_joined = filters.DateTimeFromToRangeFilter()

    o = filters.OrderingFilter(fields=['date_joined', ])

    class Meta:
        model = Account
        fields = ['phone_number', 'is_active', 'is_superuser', 'is_moderator', 'date_joined']
