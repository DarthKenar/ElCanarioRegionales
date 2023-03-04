from django.contrib import admin
from . import models
# Register your models here.

class ProductosAdmin(admin.ModelAdmin):
    list_display = ("nombre","categoria","color","material","talle","precio_compra","incremento","precio_venta")
    search_fields = ("nombre","categoria")
    list_filter = ["categoria"]
    ordering = ['nombre']
class AdminStock(admin.ModelAdmin):
    list_display = ("producto","existencias")

class AdminCliente(admin.ModelAdmin):
    list_display = ("nombre","numero_telefonico","domicilio","correo","total_comprado")
class AdminPromo(admin.ModelAdmin):
    list_display = ("nombre","productos","precio_venta")
class AdminPedido(admin.ModelAdmin):
    list_display = ("fecha","cliente","productos","cantidad_de_productos","total_a_pagar")
class AdminGasto(admin.ModelAdmin):
    list_display = ("nombre","descripcion","cantidad","precio")

class AdminColores(admin.ModelAdmin):
    list_display = ("nombre",)


admin.site.register(models.Producto, ProductosAdmin)
admin.site.register(models.Cliente, AdminCliente)
admin.site.register(models.Stock, AdminStock)
admin.site.register(models.Promo, AdminPromo)
admin.site.register(models.Pedido, AdminPedido)
admin.site.register(models.Gasto, AdminGasto)
admin.site.register(models.Colores, AdminColores)





