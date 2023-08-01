from django.urls import path
from orders.views import orders
orders_urlpatterns = ([
    path('orders', orders, name="orders"),
], 'orders')