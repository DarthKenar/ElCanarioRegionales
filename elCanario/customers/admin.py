from django.contrib import admin
from customers.models import Customer
# Register your models here.
class AdminCustomer(admin.ModelAdmin):
    list_display=['name','phone_number','address','email','total_purchased']

admin.site.register(Customer,AdminCustomer)
