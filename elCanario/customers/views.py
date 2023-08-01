from django.shortcuts import render
from customers.models import Customer
from elCanario.utils import render_login_required, string_is_empty, get_customers_for_search_input_in_native_datatype, get_customers_by_native_datatype
# Create your views here.

def customers(request):

    template="customers.html"

    customers = Customer.objects.all()

    answer = "Customers in Database"
    context = {
                "customers_any": customers,
                "answer":answer,
                "datatype_input": 'name',
                "datatype": 'Name'
               }

    return render_login_required(request, template, context)
