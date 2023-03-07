from django.contrib import admin
from .models import User
# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display = ['username','email','phone_number','password']

admin.site.register(User, AdminUser)