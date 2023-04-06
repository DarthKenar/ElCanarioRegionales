from django.contrib import admin
from .models import Categories, Values, Articles, ArticlesValues, Customers, Stocks, Promotions, Orders, Expenses

# Register your models here.

class AdminCategories(admin.ModelAdmin):
    list_display=['name']
    search_fields = ["name"]
    list_filter = ["name"]
    ordering = ['name']

class AdminValues(admin.ModelAdmin):
    list_display=['name', 'category_id']

class AdminArticles(admin.ModelAdmin):
    list_display=['name','buy_price','increase','sell_price']
    ordering = ['sell_price']

class AdminArticlesValues(admin.ModelAdmin):
    list_display=['article_id','value_id','category_id']
    


class AdminCustomers(admin.ModelAdmin):
    list_display=['name','phone_number','address','email','total_purchased']

class AdminStocks(admin.ModelAdmin):
    list_display=['article_id','stock']


class AdminPromotions(admin.ModelAdmin):
    list_display=['promotion_name','discount','sell_price', 'remainder']

class AdminOrders(admin.ModelAdmin):
    list_display=['customer_id','articles_quantity','total_pay','details','creation_date','updated_date','delivery_status']

class AdminExpenses(admin.ModelAdmin):
    list_display=['name','description','quantity','total_cost']



admin.site.register(Categories, AdminCategories)
admin.site.register(Values, AdminValues)
admin.site.register(Articles, AdminArticles)
admin.site.register(ArticlesValues, AdminArticlesValues)

admin.site.register(Customers,AdminCustomers)
admin.site.register(Stocks,AdminStocks)
admin.site.register(Promotions,AdminPromotions)
admin.site.register(Orders,AdminOrders)
admin.site.register(Expenses,AdminExpenses)



