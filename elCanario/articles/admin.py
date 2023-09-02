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
    list_display=['name','buy_price','increase','sell_price','stock']
    ordering = ['sell_price']

class AdminArticleValue(admin.ModelAdmin):
    list_display=['article_id','value_id','category_id']

class AdminPromotion(admin.ModelAdmin):
    list_display=['name','discount','sell_price', 'remainder']

admin.site.register(Category, AdminCategory)
admin.site.register(Value, AdminValue)
admin.site.register(Article, AdminArticle)
admin.site.register(ArticleValue, AdminArticleValue)
admin.site.register(Promotion,AdminPromotion)

