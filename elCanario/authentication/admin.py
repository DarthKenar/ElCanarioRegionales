from django.contrib import admin
from .models import CustomUser
# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display = ['picture']

admin.site.register(CustomUser, AdminUser)