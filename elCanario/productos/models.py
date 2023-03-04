from django.db import models
from ..authentication import models as auth_models
# Create your models here.
class Categorias(models.Model):
    nombre_categoría = models.CharField(verbose_name="Categoría", max_length=30, unique=True)
    def __str__(self) -> str:
        return f"{self.nombre_talle}"
    
class Colores(models.Model):
    nombre_color = models.CharField(verbose_name="Color", max_length=30, unique=True)
    def __str__(self) -> str:
        return f"{self.nombre_color}"
    
    
class Materiales(models.Model):
    nombre_material = models.CharField(verbose_name="Material", max_length=30, unique=True)
    def __str__(self) -> str:
        return f"{self.nombre_material}"
    
class Talles(models.Model):
    nombre_talle = models.CharField(verbose_name="Talle", max_length=32, unique=True)
    def __str__(self) -> str:
        return f"{self.nombre_talle}"

class Producto(models.Model):

    nombre = models.CharField(verbose_name="Nombre", max_length=32)

    categoria = models.ForeignKey(Categorias, verbose_name="Tipo", max_length=32, on_delete=models.DO_NOTHING)
    color = models.ForeignKey(Colores, verbose_name="Color", max_length=32, on_delete=models.DO_NOTHING)
    material = models.ForeignKey(Materiales, verbose_name="Material", max_length=32, on_delete=models.DO_NOTHING)
    talle = models.ForeignKey(Talles, verbose_name="Talle", max_length=32, on_delete=models.DO_NOTHING)

    precio_compra = models.FloatField(verbose_name="$ COMPRA")
    incremento = models.FloatField(verbose_name="Incremento del Precio", help_text=f"Numero que hace referencia al porcentaje de incremento", default=1.7)
    precio_venta = models.FloatField(verbose_name="$ VENTA", help_text="Es el resultante del precio de compra multiplicado su incremento.")

    def descripcion(self):
        return f"{self.nombre} , {self.categoria}"
    
    def __str__(self) -> str:
        return self.descripcion()
    class Meta:

        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre','categoria']

class Cliente(models.Model):

    nombre = models.CharField(verbose_name="Nombre", max_length=32)
    numero_telefonico = models.CharField(verbose_name="Numero de Teléfono", max_length=32, help_text="Este es un campo de texto en el cual se debe ingresar el numero de teléfono del cliente")
    domicilio = models.CharField(verbose_name="Domicilio", max_length=128, help_text="Este es un campo de texto en el cual se debe ingresar el domicilio del cliente")
    correo = models.EmailField(verbose_name="Correo Electrónico", default="nombre@correo.com")
    total_comprado = models.IntegerField(verbose_name="Total Comprado", editable=False, null=True, default=0)

    
class Stock(models.Model):
    
    producto = models.ForeignKey(Producto,verbose_name="Producto", on_delete=models.CASCADE) 
    existencias = models.PositiveSmallIntegerField(verbose_name="Existencias") #Values from 0 to 32767

class Promo(models.Model):
    
    nombre = models.CharField(verbose_name="Nombre",max_length=32)
    productos = models.ForeignKey(Producto, verbose_name="Productos", on_delete=models.CASCADE)
    descuento = models.PositiveSmallIntegerField(verbose_name="Descuento")
    precio_venta = models.PositiveSmallIntegerField(verbose_name="$ VENTA")


class Pedido(models.Model):

    fecha = models.DateField(auto_now=True)
    cliente = models.ForeignKey(Cliente,verbose_name="Cliente", on_delete=models.CASCADE)
    productos = models.list(Producto, verbose_name="Productos", on_delete=models.CASCADE)
    cantidad_de_productos = models.PositiveSmallIntegerField(verbose_name="Cantidad de Productos", editable=False)
    total_a_pagar = models.PositiveIntegerField(verbose_name="Total a pagar", editable=False)
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)
    estado_de_entrega = models.BooleanField(verbose_name="Estado de la entrega", default=False)
    empleado = models.ForeignKey(to=auth_models.User,verbose_name="Cargado por")

class Gasto(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=32)
    descripcion = models.CharField(verbose_name="Descripcion", max_length=128, blank=True, null=True, help_text="breve descripción del gasto si fuese necesario. *Campo NO obligatorio")
    cantidad = models.PositiveSmallIntegerField(verbose_name="Cantidad", default=1, help_text="Cantidad de productos comprados")
    precio = models.PositiveIntegerField(verbose_name="Precio", help_text="Precio de compra del producto adquirido.")

"""La idea que no se imprementar es que cuando un cliente compre, a este se le suma en "total_comprado" el total gastado por el cliente.


"""