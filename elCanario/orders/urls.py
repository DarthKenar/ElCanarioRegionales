from django.urls import path
from orders.views import OrderListView, OrderCreateTemplate, OrderUpdateTemplate, OrderCreateView, ReadDataListView, ReadDataTypeListView,OrderUpdateView, order_delete

app_name = 'orders'
urlpatterns = [
    path('read', OrderListView.as_view(), name="orders"),
    path('read_data', ReadDataListView.as_view(), name="read_data"),
    path('read_datatype', ReadDataTypeListView.as_view(), name="read_datatype"),

    path('create', OrderCreateView.as_view(), name="create"), #for GET
    path('create_form', OrderCreateTemplate.as_view(), name="create_htmx"), #for POST

    path('update/<int:pk>', OrderUpdateView.as_view(), name="update"),
    path('update_form/<int:pk>/', OrderUpdateTemplate.as_view(), name="update_htmx"),
    
    path('delete/<int:pk>', order_delete, name="delete"),
]