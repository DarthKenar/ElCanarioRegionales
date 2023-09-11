from django.urls import path
from orders.views import OrderListView, OrderCreateView, ReadDataListView, ReadDataTypeListView
app_name = 'orders'
urlpatterns = [
    path('read', OrderListView.as_view(), name="orders"),
    path('read_data', ReadDataListView.as_view(), name="read_data"),
    path('read_datatype', ReadDataTypeListView.as_view(), name="read_datatype"),
    path('create', OrderCreateView.as_view(), name="create"),
    # path('update/<int:pk>', OrderListView.as_view(), name="update"),
    # path('delete/<int:pk>', OrderListView.as_view(), name="delete"),

]