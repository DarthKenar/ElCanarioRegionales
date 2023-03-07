from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(verbose_name="Nombre", max_length=32)
    email = models.EmailField(verbose_name="Correo Electrónico", max_length=32)
    phone_number = models.CharField(verbose_name="numero de teléfono", max_length=32)
    password = models.CharField(verbose_name="Password", max_length=32)



