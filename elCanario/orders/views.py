from django.shortcuts import render
from django.urls import reverse_lazy
from typing import Any, Dict, List
from elCanario.utils import render_login_required
from orders.utils import get_orders_for_search_input, get_context_for_search_input_in_orders_section, get_context_for_datatype_input_in_orders_section
from django.http import HttpRequest, HttpResponse
from django.forms.models import BaseModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.db.models.query import QuerySet
from django.views.generic import CreateView
from orders.models import Order, ArticleOrder
from messageslog.models import MessageLog
# Create your views here.
# # ORDERS SECTION

class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['datatype_input'] = 'order_id'
        context["datatype"] = 'ID'
        context["answer"] = "Orders in Database"
        return context
    
class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'orders_create.html'
    success_url = reverse_lazy('orders:orders')
    fields=['customer_id', 'articles_cart', 'details', 'delivery_status']

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        customer_id = form.cleaned_data['customer_id']
        articles_cart = form.cleaned_data['articles_cart']
        print(articles_cart)
        print(type(articles_cart))
        details = form.cleaned_data['details']
        message = MessageLog(info=f"Order created:\n\tCustomer: {customer_id.name}, articles: {articles_cart}, details: {details}")
        message.save()
        return super().form_valid(form)
    
class ReadDataListView(ListView):
    model = Order
    template_name = 'orders_search_data.html'

    def get_queryset(self) -> QuerySet[Any]:
        search_input = self.request.GET["search_input"].strip()
        datatype_input = self.request.GET["datatype_input"].strip()
        return get_orders_for_search_input(datatype_input, search_input)
                
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        search_input = self.request.GET["search_input"].strip()
        datatype_input = self.request.GET["datatype_input"].strip()
        context["search_input"] = search_input
        context.update(get_context_for_search_input_in_orders_section(datatype_input,search_input))
        return context
    
class ReadDataTypeListView(ListView):
    model = Order
    template_name = 'orders_search_datatype.html'

    def get_queryset(self):
        datatype_input = self.request.GET["datatype_input"].strip()
        return get_orders_for_search_input(datatype_input,"")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        datatype_input = self.request.GET["datatype_input"].strip()
        context.update(get_context_for_datatype_input_in_orders_section(datatype_input))
        return context