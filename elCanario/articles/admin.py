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

class AdminStock(admin.ModelAdmin):
    list_display=['article_id','stock']


class AdminPromotion(admin.ModelAdmin):
    list_display=['name','discount','sell_price', 'remainder']



class AdminExpense(admin.ModelAdmin):
    list_display=['name','description','quantity','total_cost']
# class AdminOrdersArticles(admin.ModelAdmin):
#     list_display=['article_id','orders_id']




admin.site.register(Category, AdminCategory)
admin.site.register(Value, AdminValue)
admin.site.register(Article, AdminArticle)
admin.site.register(ArticleValue, AdminArticleValue)

admin.site.register(Stock,AdminStock)
admin.site.register(Promotion,AdminPromotion)

admin.site.register(Expense,AdminExpense)
# admin.site.register(OrdersArticles,AdminOrdersArticles)


