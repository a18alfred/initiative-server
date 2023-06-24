from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.apps.accounts'

    # Зарегистрируем сигналы
    def ready(self):
        import core.apps.accounts.signals
