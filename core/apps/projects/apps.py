from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.apps.projects'

    # Зарегистрируем сигналы
    def ready(self):
        import core.apps.projects.signals
