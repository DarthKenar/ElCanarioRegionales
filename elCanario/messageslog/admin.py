from django.contrib import admin
from messageslog.models import MessageLog
# Register your models here.
class AdminMessageLog(admin.ModelAdmin):
    list_display = ['info','date']

admin.site.register(MessageLog, AdminMessageLog)