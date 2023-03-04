from django.db import models

# Create your models here.
class User(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=32)
    correo = models.EmailField(verbose_name="Correo Electrónico", max_length=32)
    telefono = models.CharField(verbose_name="numero de teléfono", max_length=32)
    contrasenia = models.CharField(verbose_name="Password", max_length=32)



