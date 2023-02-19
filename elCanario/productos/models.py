from django.db import models

# Create your models here.
class Stock(models.Model):

    colores = (("VDE","verde"),("BDO","bordó"),("AZL","azul"),("NRA","negra"),("BCA","blanca"),("BGE","beige"))
    nombre = models.CharField(verbose_name="Nombre", max_length=32)
    tipo = models.CharField(verbose_name="Tipo", max_length=32)
    color = models.CharField(verbose_name="Color",null=True, blank=True, max_length=32, choices=colores)
    material = models.CharField(verbose_name="Material", null=True, blank=True, max_length=32)
    talle = models.IntegerField(verbose_name="Talle", null=True, blank=True)
    precio_compra = models.FloatField(verbose_name="Precio de Compra")
    incremento = models.FloatField(verbose_name="Incremento del Precio")
    precio_venta = models.FloatField(verbose_name="Precio de Venta")


class Pedidos(models.Model):
    pass

class Promos(models.Model):
    pass

class Gastos(models.Model):
    pass

class Clientes(models.Model):
    pass


