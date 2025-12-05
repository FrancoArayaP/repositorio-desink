from django.apps import AppConfig


class DesinkappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'desinkApp'


class DesinkappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'desinkApp'

    def ready(self):
        import desinkApp.signals

