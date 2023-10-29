import decimal
from django.shortcuts import render
from django.urls import reverse_lazy
from typing import Any, Dict, List
from django.utils.translation import gettext_lazy as _
from orders.form import OrderForm
from django.shortcuts import get_object_or_404
from elCanario.utils import render_login_required
from orders.utils import update_total_purchased, update_article_quantity,update_total_pay, get_orders_for_search_input, get_context_for_search_input_in_orders_section, get_context_for_datatype_input_in_orders_section
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.db.models.query import QuerySet
from django.views.generic import CreateView, UpdateView, TemplateView
from orders.models import Order
from django.views.decorators.csrf import csrf_protect
from messageslog.models import MessageLog
# Create your views here.
# # ORDERS SECTION

class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['datatype_input'] = 'id'
        context["datatype"] = 'ID'
        context["answer"] = _("Orders in Database")
        return context
    
class ReadDataListView(LoginRequiredMixin, ListView):
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


class ReadDataTypeListView(LoginRequiredMixin, ListView):
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


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders_create.html'
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.template_name = "create_form.html"
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form: OrderForm) -> HttpResponse:
        customer_id = form.cleaned_data['customer_id']
        articles_cart = form.cleaned_data['articles_cart']
        details = form.cleaned_data['details']
        message = MessageLog(info=_(f"Order created:\n\tCustomer: {customer_id.name}, articles: {articles_cart}, details: {details}"))
        message.save()
        return super().form_valid(form) #Esto hace que se guarde.

    def get_success_url(self) -> str:
        update_article_quantity(self.object)
        update_total_pay(self.object)
        update_total_purchased(self.object)
        return reverse_lazy('orders:create_htmx') + '?success'


class OrderCreateTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'create_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = OrderForm()
        context['form'] = form
        return context

    
class OrderUpdateView(LoginRequiredMixin,UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders_update.html'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.template_name = "update_form.html"
        return super().post(request, *args, **kwargs)

    def form_valid(self, form: OrderForm) -> HttpResponse:
        customer_id = form.cleaned_data['customer_id']
        articles_cart = form.cleaned_data['articles_cart']
        details = form.cleaned_data['details']
        message = MessageLog(info=_(f"Order Edited:\n\tCustomer: {customer_id.name}, articles: {articles_cart}, details: {details}"))
        message.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        update_article_quantity(self.object)
        update_total_pay(self.object)
        update_total_purchased(self.object)
        return reverse_lazy('orders:update_htmx', args=[f"{self.object.id}"]) + '?success'


class OrderUpdateTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objeto_id = self.kwargs.get('pk')
        object = get_object_or_404(Order,id=objeto_id)
        context['object'] = object
        form = OrderForm(instance=object) 
        context['form'] = form
        return context


@csrf_protect
def order_delete(request:object, pk:int)-> HttpResponse:
    template = 'orders_search_data.html'
    context = {}
    try:
        order = get_object_or_404(Order, id=pk)
    except Exception as e:
        context["delete_answer"] = _(f"The selected order could not be deleted because it does not exist. Contact support.")
        return render_login_required(request, template, context)
    else:
        context["delete_answer"] = _(f"Order {order.pk} for {order.customer_id} has been eliminated")
        message = MessageLog(info=_(f"Order {order.pk} for {order.customer_id} has been eliminated"))
        message.save()
        order.delete()
        orders = Order.objects.all()
        context.update({"object_list": orders})
        return render_login_required(request, template, context)