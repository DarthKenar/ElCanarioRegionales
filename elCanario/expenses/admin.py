from django.contrib import admin
from expenses.models import Expense
# Register your models here.

class AdminExpense(admin.ModelAdmin):
    list_display=['name','description','quantity','total_cost']

admin.site.register(Expense,AdminExpense)