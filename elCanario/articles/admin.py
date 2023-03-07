from django.contrib import admin
from . import models
# Register your models here.

class AdminArticles(admin.ModelAdmin):
    list_display = ("article_name","category_id","color_id","material_id","size_id","buy_price","increase","sell_price")
    search_fields = ("article_name","category_id")
    list_filter = ["category_id"]
    ordering = ['article_name']

class AdminStocks(admin.ModelAdmin):
    list_display = ("article_id","stock")

class AdminCustomers(admin.ModelAdmin):
    list_display = ("customer_name","phone_number","address","email","total_purchased")
class AdminPromotions(admin.ModelAdmin):
    list_display = ("promotion_name","articles_id","discount","sell_price")
class AdminOrders(admin.ModelAdmin):
    list_display = ("customer_id","article_id","articles_quantity","total_pay","creation_date","delivery_status")
class AdminExpenses(admin.ModelAdmin):
    list_display = ("expense_name","description","quantity","total_cost")
##

class AdminColors(admin.ModelAdmin):
    list_display = ("color_name",)

class AdminCategories(admin.ModelAdmin):
    list_display = ("category_name",)

class AdminMaterials(admin.ModelAdmin):
    list_display = ("material_name",)

class AdminSizes(admin.ModelAdmin):
    list_display = ("size_name",)


admin.site.register(models.Articles, AdminArticles)
admin.site.register(models.Stocks, AdminStocks)
admin.site.register(models.Customers, AdminCustomers)
admin.site.register(models.Promotions, AdminPromotions)
admin.site.register(models.Orders, AdminOrders)
admin.site.register(models.Expenses, AdminExpenses)
admin.site.register(models.Colors, AdminColors)
admin.site.register(models.Categories, AdminCategories)
admin.site.register(models.Materials, AdminMaterials)
admin.site.register(models.Sizes, AdminSizes)







