from django.urls import path
from customers.views import CustomerListView, ReadDataListView, CustomerCreateView, ReadDataTypeListView
from customers.views import NameCheckView, DniCheckView, PhoneNumberCheckView, AddressCheckView, EmailCheckView, CreateConfirmView

app_name = 'customers'
urlpatterns = [
    path('', CustomerListView.as_view(), name="customers"),
    path('customers_create', CustomerCreateView.as_view(), name="create"),
    path('read_data', ReadDataListView.as_view(), name="read_data"),
    path('read_datatype', ReadDataTypeListView.as_view(), name="read_datatype"),
    #Customer Create
    path('create_name_check',NameCheckView.as_view(),name='create_name_check'),
    path('create_dni_check',DniCheckView.as_view(),name='create_dni_check'),
    path('create_phone_number_check',PhoneNumberCheckView.as_view(),name='create_phone_number_check'),
    path('create_address_check',AddressCheckView.as_view(),name='create_address_check'),
    path('create_email_check',EmailCheckView.as_view(),name='create_email_check'),
    path('create_confirm',CreateConfirmView.as_view(),name='create_confirm')
    # path('customers_update/<int:id>', articles_views.customers_read_data_update, name="customers_update"),
    # path('customers_delete/<int:id>', articles_views.customers_read_data_delete, name="customers_delete"),
]