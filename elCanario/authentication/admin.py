from django.contrib import admin
from .models import User
# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display = ['nombre','correo','contrasenia']

admin.site.register(User, AdminUser)