from django.db import models

# Create your models here.
class Producto(models.Model):

    nombre = models.CharField(verbose_name="Nombre", max_length=32)
    categoria = models.CharField(verbose_name="Tipo", max_length=32)
    color = models.CharField(verbose_name="Color",null=True, blank=True, max_length=32)
    material = models.CharField(verbose_name="Material", null=True, blank=True, max_length=32)
    talle = models.PositiveSmallIntegerField(verbose_name="Talle", null=True, blank=True)
    precio_compra = models.FloatField(verbose_name="$ COMPRA")
    incremento = models.FloatField(verbose_name="Incremento del Precio", help_text=f"Para incrementar un 70% se debe escribir '1.7'.", default=1.7)
    precio_venta = models.FloatField(verbose_name="$ VENTA",auto_created=True, help_text="Debe ser el resultante del precio de compra multiplicado su incremento.")

    """def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)
        self.precio_venta = (self.precio_compra*self.incremento)"""


class Cliente(models.Model):

    nombre = models.CharField(verbose_name="Nombre", max_length=32)
    numero_telefonico = models.CharField(verbose_name="Numero de Teléfono", max_length=32, help_text="Este es un campo de texto en el cual se debe ingresar el numero de teléfono del cliente")
    domicilio = models.CharField(verbose_name="Domicilio", max_length=128, help_text="Este es un campo de texto en el cual se debe ingresar el domicilio del cliente")
    correo = models.EmailField(verbose_name="Correo Electrónico", default="nombre@correo.com")
    #total_comprado = models.IntegerField(verbose_name="Total Comprado")

    
class Stock(models.Model):
    
    #producto = models.ForeignKey(Producto,verbose_name="Producto", on_delete=models.CASCADE) #Revisar parametros del método ForeignKey
    existencias = models.PositiveSmallIntegerField(verbose_name="Existencias") #Values from 0 to 32767

class Promo(models.Model):
    
    nombre = models.CharField(verbose_name="Nombre",max_length=32)
    #productos = models.ForeignKey(Producto, verbose_name="Productos", on_delete=models.CASCADE)
    precio_venta = models.PositiveSmallIntegerField(verbose_name="$ VENTA")


class Pedido(models.Model):

    fecha = models.DateField(auto_now=True)
    #cliente = models.ForeignKey(Cliente,verbose_name="Cliente", on_delete=models.CASCADE)
    #productos = models.ForeignKey(Producto, verbose_name="Productos", on_delete=models.CASCADE)
    cantidad_de_productos = models.PositiveSmallIntegerField(verbose_name="",auto_created=True)
    total_a_pagar = models.PositiveIntegerField(verbose_name="Total a pagar")

    """def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        #Acá. debería agarrar el precio final de cada producto de los artículos del pedido ?=?=?"""

class Gasto(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=32)
    descripcion = models.CharField(verbose_name="Descripcion", max_length=128, blank=True, null=True, help_text="breve descripción del gasto si fuese necesario. *Campo NO obligatorio")
    cantidad = models.PositiveSmallIntegerField(verbose_name="Cantidad", default=1, help_text="Cantidad de productos comprados")
    precio = models.PositiveIntegerField(verbose_name="Precio", help_text="Precio de compra del producto adquirido.")
class Ganancias(models.Model):
    pass

"""La idea que no se imprementar es que cuando un cliente compre, a este se le suma en "total_comprado" el total gastado por el cliente.


"""