from django.contrib import admin
from orders.models import Order
# Register your models here.
class AdminOrder(admin.ModelAdmin):
    list_display=['customer_id','total_pay','details','creation_date','updated_date','delivery_status']
    
admin.site.register(Order,AdminOrder)