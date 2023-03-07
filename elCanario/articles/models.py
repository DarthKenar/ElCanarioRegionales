from django.db import models
#from ..authentication import models as auth_models
# Create your models here.
class Categories(models.Model):

    category_name = models.CharField(verbose_name="Categoría", max_length=30, unique=True)

    class Meta:

        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self) -> str:

        return f"{self.category_name}"


class Colors(models.Model):

    color_name = models.CharField(verbose_name="Color", max_length=30, unique=True)

    def __str__(self) -> str:

        return f"{self.color_name}"
    
    class Meta:

        verbose_name = "Color"
        verbose_name_plural = "Colores"
    

class Materials(models.Model):

    material_name = models.CharField(verbose_name="Material", max_length=30, unique=True)

    def __str__(self) -> str:

        return f"{self.material_name}"
    
    class Meta:

        verbose_name = "Material"
        verbose_name_plural = "Materiales"


class Sizes(models.Model):

    size_name = models.CharField(verbose_name="Talle", max_length=32, unique=True)

    def __str__(self) -> str:

        return f"{self.size_name}"
    
    class Meta:

        verbose_name = "Talle"
        verbose_name_plural = "Talles"


class Articles(models.Model):

    article_name = models.CharField(verbose_name="Nombre", max_length=32)
    category_id = models.ForeignKey(Categories, verbose_name="Categoría", max_length=32,blank=True, null=True ,on_delete=models.DO_NOTHING)
    color_id = models.ForeignKey(Colors, verbose_name="Color", max_length=32,blank=True , null=True,on_delete=models.DO_NOTHING)
    material_id = models.ForeignKey(Materials, verbose_name="Material", max_length=32,blank=True, null=True , on_delete=models.DO_NOTHING)
    size_id = models.ForeignKey(Sizes, verbose_name="Talle", max_length=32,blank=True, null=True , on_delete=models.DO_NOTHING)
    buy_price = models.FloatField(verbose_name="$ COMPRA")
    increase = models.FloatField(verbose_name="Incremento del Precio", help_text=f"Numero que hace referencia al porcentaje de incremento", default=1.7)
    sell_price = models.FloatField(verbose_name="$ VENTA", help_text="Es el resultante del precio de compra multiplicado su incremento.")

    class Meta:

        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        ordering = ['article_name','category_id']
    
    def description(self):

        return f"{self.article_name} , {self.category_id}"
    
    def __str__(self) -> str:

        return self.description()


class Customers(models.Model):

    customer_name = models.CharField(verbose_name="Cliente", max_length=32)
    phone_number = models.CharField(verbose_name="Numero de Teléfono", max_length=32, help_text="Este es un campo de texto en el cual se debe ingresar el numero de teléfono del cliente")
    address = models.CharField(verbose_name="Domicilio", max_length=128,blank=True, null=True ,default="Avenida siempre viva", help_text="Este es un campo de texto en el cual se debe ingresar el domicilio del cliente")
    email = models.EmailField(verbose_name="Correo Electrónico",blank=True, null=True , default="nombre@correo.com")
    total_purchased = models.FloatField(verbose_name="Total Comprado", editable=False, blank=True,null=True, default=0)

    class Meta:

        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['customer_name',]
    
    def __str__(self) -> str:

        return f"{self.customer_name}, {self.phone_number}"


class Stocks(models.Model):
    
    article_id = models.ForeignKey(Articles,verbose_name="Artículo", on_delete=models.CASCADE, unique=True) 
    stock = models.PositiveSmallIntegerField(verbose_name="Existencias") #Values from 0 to 32767

    class Meta:

        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ['article_id','stock']
    
    def __str__(self) -> str:

        return f"{self.article_id}, {self.stock}"


class Promotions(models.Model):
    
    promotion_name = models.CharField(verbose_name="Nombre",max_length=32)
    articles_id = models.ForeignKey(Articles, verbose_name="Productos", on_delete=models.CASCADE)
    discount = models.FloatField(verbose_name="Descuento")
    sell_price = models.FloatField(verbose_name="$ VENTA")

    class Meta:

        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"
        ordering = ['promotion_name','articles_id']
    
    def __str__(self) -> str:

        return f"{self.promotion_name}, {self.articles_id}, {self.discount}, {self.sell_price}"


class Orders(models.Model):

    customer_id = models.ForeignKey(Customers,verbose_name="Cliente", on_delete=models.CASCADE)
    article_id = models.ForeignKey(Articles, verbose_name="Artículos", on_delete=models.CASCADE)
    articles_quantity = models.PositiveSmallIntegerField(verbose_name="Cantidad de Artículos", editable=False, blank=True, null=True)
    total_pay = models.PositiveIntegerField(verbose_name="Total a pagar", editable=False, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    delivery_status = models.BooleanField(verbose_name="Estado de la entrega", default=False)
    #created_by = models.ForeignKey(to=auth_models.User,verbose_name="Cargado por") (NO SE PUEDE HCER ESTO YA QUE TRAE LA INFORMACION DESDE OTRA APP)

    class Meta:

        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['customer_id',]
    
    def __str__(self) -> str:

        return f"{self.customer_id}, {self.article_id}, {self.articles_quantity}"


class Expenses(models.Model):

    expense_name = models.CharField(verbose_name="Nombre", max_length=32)
    description = models.CharField(verbose_name="Descripcion", max_length=128, blank=True, null=True, help_text="breve descripción del gasto si fuese necesario. *Campo NO obligatorio")
    quantity = models.PositiveSmallIntegerField(verbose_name="Cantidad", default=1, help_text="Cantidad de productos comprados")
    total_cost = models.FloatField(verbose_name="Precio", help_text="Precio de compra del producto adquirido.")

    class Meta:

        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"
        ordering = ['total_cost','expense_name']
    
    def __str__(self) -> str:

        return f"{self.expense_name},{self.description},{self.quantity},{self.total_cost}"
    
"""La idea que no se imprementar es que cuando un cliente compre, a este se le suma en "total_comprado" el total gastado por el cliente."""