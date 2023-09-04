from django.urls import path
from customers.views import CustomerListView, ReadDataListView, CustomerCreateView, ReadDataTypeListView

app_name = 'customers'
urlpatterns = [
    path('', CustomerListView.as_view(), name="customers"),
    path('customers_create', CustomerCreateView.as_view(), name="create"),
    path('read_data', ReadDataListView.as_view(), name="read_data"),
    path('read_datatype', ReadDataTypeListView.as_view(), name="read_datatype"),
    # path('customers_update/<int:id>', articles_views.customers_read_data_update, name="customers_update"),
    # path('customers_delete/<int:id>', articles_views.customers_read_data_delete, name="customers_delete"),
]