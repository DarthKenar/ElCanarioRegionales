from django.contrib import admin
from orders.models import Order, ArticleOrder
# Register your models here.
class AdminOrder(admin.ModelAdmin):
    list_display=['customer_id','total_pay','details','creation_date','updated_date','delivery_status']

class AdminArticleOrder(admin.ModelAdmin):
    list_display=['article_id', 'order_id']
    
admin.site.register(Order,AdminOrder)
admin.site.register(ArticleOrder,AdminArticleOrder)