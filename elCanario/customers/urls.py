from django.urls import path
from customers.views import customers
customers_urlpatterns = ([
    path('customers', customers, name="customers"),
    # path('customers', articles_views.customers, name="customers"),
    # path('customers_create', articles_views.customers_create, name="customers_create"),
    # path('customers_read_datatype', articles_views.customers_read_datatype, name="customers_read_datatype"),
    # path('customers_read_data', articles_views.customers_read_data, name="customers_read_data"),
    # path('customers_update/<int:id>', articles_views.customers_read_data_update, name="customers_update"),
    # path('customers_delete/<int:id>', articles_views.customers_read_data_delete, name="customers_delete"),
], 'customers')