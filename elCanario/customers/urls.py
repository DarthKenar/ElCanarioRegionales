from django.urls import path
from customers.views import ReadDataListView, CustomerCreateTemplate, CustomerUpdateTemplate, CustomerListView, CustomerCreateView, ReadDataTypeListView,CustomerUpdateView
from customers.views import customer_delete

app_name = 'customers'
urlpatterns = [
    path('read', CustomerListView.as_view(), name="customers"),
    path('read_data', ReadDataListView.as_view(), name="read_data"),
    path('read_datatype', ReadDataTypeListView.as_view(), name="read_datatype"),

    path('create', CustomerCreateView.as_view(), name="create"),
    path('create_form', CustomerCreateTemplate.as_view(), name="create_htmx"),

    path('update/<int:pk>/', CustomerUpdateView.as_view(), name="update"),
    path('update_form/<int:pk>/', CustomerUpdateTemplate.as_view(), name="update_htmx"),

    path('delete/<int:pk>', customer_delete, name="delete"),
]