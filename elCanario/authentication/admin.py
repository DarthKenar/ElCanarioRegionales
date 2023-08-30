from django.contrib import admin
from .models import UserProfileExtends
# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display = ['user','profile_picture']

admin.site.register(UserProfileExtends, AdminUser)