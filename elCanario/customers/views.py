from django.shortcuts import render
from typing import Any, Dict
from customers.models import Customer
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from elCanario.utils import render_login_required, string_is_empty, get_customers_for_search_input_in_native_datatype, get_customers_by_native_datatype
# Create your views here.

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers.html'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["datatype"] = 'Nombre'
        context["answer"] = "Customers in Database"
        return context

