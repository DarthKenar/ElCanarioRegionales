from django.urls import path
from customers.views import CustomerListView, ReadDataListView, CustomerCreateView, CustomerCreateTemplate, ReadDataTypeListView,CustomerUpdateView
from customers.views import customer_delete, CustomerUpdateTemplate

app_name = 'customers'
urlpatterns = [
    path('', CustomerListView.as_view(), name="customers"),
    path('create', CustomerCreateView.as_view(), name="create"),
    path('create/<str:status>', CustomerCreateView.as_view(), name="create"),
    path('create_form', CustomerCreateTemplate.as_view(), name="create_htmx"),
    path('update/<int:pk>/', CustomerUpdateView.as_view(), name="update"),
    path('update/<int:pk>/<str:status>', CustomerUpdateView.as_view(), name="update"),
    path('update_form/<int:pk>/', CustomerUpdateTemplate.as_view(), name="update_htmx"),
    path('read_data', ReadDataListView.as_view(), name="read_data"),
    path('read_datatype', ReadDataTypeListView.as_view(), name="read_datatype"),
    path('delete/<int:pk>', customer_delete, name="delete"),
    # path('create_confirm',CreateConfirmView.as_view(),name='create_confirm')
    # path('customers_update/<int:id>', articles_views.customers_read_data_update, name="customers_update"),
    # path('customers_delete/<int:id>', articles_views.customers_read_data_delete, name="customers_delete"),
]