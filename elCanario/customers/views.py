from django.shortcuts import render
from typing import Any, Dict
from customers.models import Customer
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from customers.utils import get_context_for_search_input_in_customers_section, get_customers_for_search_input, string_is_empty
from elCanario.utils import render_login_required, string_is_empty
# Create your views here.

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers.html'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["datatype"] = 'Nombre'
        context["answer"] = "Customers in Database"
        return context
    

class CustomerCreateView(TemplateView):
    template_name = 'customers_create.html'


class ReadDataListView(LoginRequiredMixin, ListView):
    template_name = 'customers_search_data.html'
    model = Customer

    def get_queryset(self) -> QuerySet[Any]:
        search_input = self.request.GET["search_input"].strip()
        datatype_input = self.request.GET["datatype_input"].strip()

        if string_is_empty(search_input):
            return Customer.objects.all()
        else:
            return get_customers_for_search_input(datatype_input, search_input)
                
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        search_input = self.request.GET["search_input"].strip()
        datatype_input = self.request.GET["datatype_input"].strip()
        context["search_input"] = search_input
        context.update(get_context_for_search_input_in_customers_section(datatype_input,search_input))
        return context

