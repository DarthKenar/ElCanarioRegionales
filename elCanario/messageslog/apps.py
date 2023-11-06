from django.apps import AppConfig


class MessageslogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messageslog'

    def ready(self):
        import messageslog.signals