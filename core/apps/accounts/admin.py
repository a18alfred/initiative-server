from django.contrib import admin
from .models import Account, Profile, PhoneCodeVerification


class ProfileInline(admin.StackedInline):
    model = Profile
    fieldsets = [
        (None, {
            'fields': ['first_name', 'middle_name', 'last_name', 'email']}),
    ]

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False


class PhoneCodeVerificationInline(admin.StackedInline):
    model = PhoneCodeVerification
    readonly_fields = ['created_at', 'checked_number']
    fieldsets = [
        (None, {
            'fields': ['code', 'created_at', 'checked_number']}),
    ]

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False


class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'phone_number', 'date_joined', 'last_login']
    fieldsets = [
        (None, {'fields': ['id', 'is_phone_confirmed', 'is_active', ]}),
        ('Права',
         {'fields': ['is_moderator', ]}),
        ('Суперпользователь',
         {'fields': ['is_superuser', 'is_staff']}),
        ('Даты',
         {'fields': ['date_joined', 'last_login']}),

    ]

    inlines = [ProfileInline, PhoneCodeVerificationInline]
    list_display = ('phone_number', 'is_active', 'is_moderator', 'date_joined',)
    list_filter = ['date_joined', 'is_active', 'is_moderator', 'is_superuser', ]
    search_fields = ['phone_number', 'id']


admin.site.register(Account, AccountAdmin)
