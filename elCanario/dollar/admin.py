from django.contrib import admin
from models import DollarGraph
# Register your models here.
class AdminDollarGraph(admin.ModelAdmin):
    list_display = ['id','price','date']
admin.site.register(DollarGraph,AdminDollarGraph)
