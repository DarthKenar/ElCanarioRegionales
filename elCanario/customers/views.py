from customers.forms import CustomerForm
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _
from urllib.parse import parse_qs
from typing import Any, Dict, List
from django.urls import reverse_lazy
from customers.models import Customer
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from customers.utils import get_context_for_search_input_in_customers_section, get_customers_for_search_input, get_context_for_datatype_input_in_customers_section
from elCanario.utils import render_login_required


class CustomerListView(LoginRequiredMixin, ListView):
    """List all existing customers

    Args:
        LoginRequiredMixin: Allow access to the view for registered users only.
        ListView: ListView Generic

    Returns:
        HttpResponse: /read
    """
    model = Customer
    template_name = 'customers.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['datatype_input'] = 'name'
        context["datatype"] = _('Name')
        context["answer"] = _("Customers in Database")
        return context


class ReadDataListView(LoginRequiredMixin, ListView):
    """Lists all existing cutomers that match the specific value entered/selected (Data).
    For example: Assuming that the Cutomer Model has a "Name" attribute
    DataType: Name
    Data: James

    Args:
        LoginRequiredMixin: Allow access to the view for registered users only.
        ListView: ListView Generic

    Returns:
        HttpResponse: /read_data
    """
    template_name = 'customers_search_data.html'
    model = Customer

    def get_queryset(self) -> QuerySet[Any]:
        search_input = self.request.GET["search_input"].strip()
        datatype_input = self.request.GET["datatype_input"].strip()
        return get_customers_for_search_input(datatype_input, search_input)
                
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        search_input = self.request.GET["search_input"].strip()
        datatype_input = self.request.GET["datatype_input"].strip()
        context["search_input"] = search_input
        context.update(get_context_for_search_input_in_customers_section(datatype_input,search_input))
        return context


class ReadDataTypeListView(LoginRequiredMixin, ListView):
    """Lists all existing Customer that match the selected Data Type, corresponding attribute of the Customer model.
    For example: Assuming that the Customer model has an attribute "Name"
    Data Type: Name
    Data: ...

    Args:
        LoginRequiredMixin: Allow access to the view only to registered users.
        ListView: Generic ListView

    Returns:
        HttpResponse: /read_datatype
    """
    model = Customer
    template_name = 'customers_search_datatype.html'

    def get_queryset(self):
        datatype_input = self.request.GET["datatype_input"].strip()
        return get_customers_for_search_input(datatype_input,"")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        datatype_input = self.request.GET["datatype_input"].strip()
        context.update(get_context_for_datatype_input_in_customers_section(datatype_input))
        return context


class CustomerCreateView(LoginRequiredMixin, CreateView):
    """Redirects the user to create an Customer in case you use the GET method, if you use the POST method it is assumed that you are already in the form checking the fields and saving the customer if possible.

    Args:
        LoginRequiredMixin: Allow access to the view for registered users only.
        CreateView: CreateView Generic

    Returns:
        HttpResponse: 
            GET: Redirects to the creation form
            POST: A portion of the html is replaced using htmx  
    """
    model = Customer
    form_class = CustomerForm
    template_name = 'customers_create.html'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.template_name = "create_form.html"
        return super().post(request, *args, **kwargs)

    def get_success_url(self) -> str:
        """
        Returns:
                HttpResponse: A part of the html is replaced with htmx replacing the old form with a new empty one.
        """
        return reverse_lazy('customers:create_htmx') + '?success'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create Customer")
        return context

class CustomerCreateTemplate(LoginRequiredMixin,TemplateView):
    """View that is used only when the CustomerCreateView creation form was successful. This view is the one used to replace one part of the html with another using htmx.

    Args:
        LoginRequiredMixin: Allow access to the view for registered users only.
        TemplateView: TemplateView Generic

    Returns:
            HttpResponse: A part of the html is replaced with htmx replacing the old form with a new empty one.
    """
    template_name = 'create_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CustomerForm()
        context["title"] = _("Create Customer")
        context['form'] = form
        return context


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    """Redirects the user to update an Customer in case you use the GET method, if you use the POST method it is assumed that you are already in the form checking the fields and updating the customer if possible.

    Args:
        LoginRequiredMixin: Allow access to the view for registered users only.
        UpdateView: UpdateView Generic

    Returns:
        HttpResponse: 
            GET: Redirects to the updating form
            POST: A portion of the html is replaced using htmx  
    """
    model = Customer
    form_class = CustomerForm
    template_name = "customers_update.html"
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.template_name = "update_form.html"
        return super().post(request, *args, **kwargs)

    def get_success_url(self) -> str:
        """
        Returns:
                HttpResponse: A part of the html is replaced with htmx replacing the old form with a new empty one.
                Success is added to the response to display a success message to the user if this word exists in the response.
        """
        return reverse_lazy('customers:update_htmx', args=[f"{self.object.id}"]) + '?success'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Update Customer")
        return context
        
class CustomerUpdateTemplate(LoginRequiredMixin, TemplateView):
    """View that is used only when the CustomerUpdateView update form is successful. This view is the one used to replace one part of the html with another using htmx.

    Args:
        LoginRequiredMixin: Allows access to the view only to registered users.
        TemplateView: TemplateView Generic

    Returns:
            HttpResponse: A part of the html is replaced by htmx replacing the old form by a new one containing the same data of the old form.
    """
    template_name = "update_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objeto_id = self.kwargs.get('pk')
        object = get_object_or_404(Customer,id=objeto_id)
        context['object'] = object
        form = CustomerForm(instance=object)
        context["title"] = _("Update Customer")
        context['form'] = form
        return context


@csrf_protect
def customer_delete(request:object, pk:int)-> HttpResponse:
    """View used for the deletion of an object of type Customer.
    - Has crsf protection.
    - Login required.
    Args:
        request (object): request
        pk (int): Identifier of the customer to be deleted.

    Returns:
        HttpResponse: returns the list of all customers in context
    """
    template = 'customers_search_data.html'
    context = {}
    try:
        customer = get_object_or_404(Customer, id=pk)
    except Exception as e:
        context["delete_answer"] = _("The selected item could not be deleted because it does not exist. Contact support.")
        return render_login_required(request, template, context)
    else:
        context["delete_answer"] = _(f"Customer {customer.name} has been eliminated")
        customer.delete()
        customers = Customer.objects.all()
        context.update({"object_list": customers})
        return render_login_required(request, template, context)
