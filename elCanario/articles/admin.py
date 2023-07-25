from django.contrib import admin
from .models import *

# Register your models here.

class AdminCategory(admin.ModelAdmin):
    list_display=['name']
    search_fields = ["name"]
    list_filter = ["name"]
    ordering = ['name']

class AdminValue(admin.ModelAdmin):
    list_display=['category_id','name']

class AdminArticle(admin.ModelAdmin):
    list_display=['name','buy_price','increase','sell_price']
    ordering = ['sell_price']

class AdminArticleValue(admin.ModelAdmin):
    list_display=['article_id','value_id','category_id']
    


class AdminCustomer(admin.ModelAdmin):
    list_display=['name','phone_number','address','email','total_purchased']

class AdminStock(admin.ModelAdmin):
    list_display=['article_id','stock']


class AdminPromotion(admin.ModelAdmin):
    list_display=['name','discount','sell_price', 'remainder']

class AdminOrder(admin.ModelAdmin):
    list_display=['customer_id','total_pay','details','creation_date','updated_date','delivery_status']

class AdminExpense(admin.ModelAdmin):
    list_display=['name','description','quantity','total_cost']
# class AdminOrdersArticles(admin.ModelAdmin):
#     list_display=['article_id','orders_id']




admin.site.register(Category, AdminCategory)
admin.site.register(Value, AdminValue)
admin.site.register(Article, AdminArticle)
admin.site.register(ArticleValue, AdminArticleValue)
admin.site.register(Customer,AdminCustomer)
admin.site.register(Stock,AdminStock)
admin.site.register(Promotion,AdminPromotion)
admin.site.register(Order,AdminOrder)
admin.site.register(Expense,AdminExpense)
# admin.site.register(OrdersArticles,AdminOrdersArticles)


