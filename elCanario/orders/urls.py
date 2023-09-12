from django.urls import path
from orders.views import OrderListView, OrderCreateView, ReadDataListView, ReadDataTypeListView,OrderCreateTemplate, OrderUpdateTemplate,OrderUpdateView, order_delete
app_name = 'orders'
urlpatterns = [
    path('read', OrderListView.as_view(), name="orders"),
    path('read_data', ReadDataListView.as_view(), name="read_data"),
    path('read_datatype', ReadDataTypeListView.as_view(), name="read_datatype"),

    path('create', OrderCreateView.as_view(), name="create"), #GET
    path('create/<str:status>', OrderCreateView.as_view(), name="create"), #POST status!
    path('create_form', OrderCreateTemplate.as_view(), name="create_htmx"), #POST render form

    path('update/<int:pk>', OrderUpdateView.as_view(), name="update"),
    path('update/<int:pk>/<str:status>', OrderUpdateView.as_view(), name="update"),
    path('update_form/<int:pk>', OrderUpdateTemplate.as_view(), name="update_htmx"),
    path('delete/<int:pk>', order_delete, name="delete"),
]