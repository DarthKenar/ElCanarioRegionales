from django.apps import AppConfig

class DollarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dollar'

    #En produccion parece mostrar un error con el wsgi... 

    # def ready(self):
    #     import dollar.tasks