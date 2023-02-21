from django.contrib import admin
from . import models
# Register your models here.

class StockAdmin(admin.ModelAdmin):
    list_display = ("nombre","tipo","color","material","talle","precio_compra","incremento","precio_venta")
    search_fields = ("nombre","tipo")
    list_filter = ["tipo"]
    ordering = ['nombre']

admin.site.register(models.Stock, StockAdmin)