from django.urls import path
from customers.views import customers
customers_urlpatterns = ([
    path('customers', customers, name="customers"),
], 'customers')