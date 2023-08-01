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

def customers_read_datatype(request):

    template = 'customers_search_datatype.html'
    context = {}
    datatype_input = request.GET['datatype_input'].strip()

    context.update(get_customers_by_native_datatype(datatype_input))

    return render_login_required(request, template, context)

def customers_read_data(request):
    
    template = "customers_search_right.html"

    search_input = request.GET["search_input"].strip()
    datatype_input = request.GET["datatype_input"].strip()
    context = {}

    if string_is_empty(search_input):
        """If the search field is empty, all items will be displayed."""
        context["articles_any"] = Customer.objects.all()

    else:
        """If the search field is not empty, it will be searched according to a native data type (not category)."""
        context.update(get_customers_for_search_input_in_native_datatype(datatype_input, search_input))

    return render_login_required(request, template, context)
def customers_create(request):
    template = 'customers_search_right.html'
    context = {}
    return render_login_required(request, template, context)