from mailbox import Message
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from typing import Any, Dict
from django.urls import reverse_lazy
from customers.models import Customer
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from messageslog.models import MessageLog
from customers.utils import get_context_for_search_input_in_customers_section, get_customers_for_search_input, get_context_for_datatype_input_in_customers_section
from elCanario.utils import render_login_required, string_is_empty
# Create your views here.

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers.html'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['datatype_input'] = 'name'
        context["datatype"] = 'Name'
        context["answer"] = "Customers in Database"
        return context
    

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    template_name = 'customers_create.html'
    success_url  = reverse_lazy('customers:customers')
    fields=['name','dni','phone_number','address','email']

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        name = form.cleaned_data['name']
        dni = form.cleaned_data['dni']
        phone_number = form.cleaned_data['phone_number']
        address = form.cleaned_data['address']
        email = form.cleaned_data['email']
        message = MessageLog(info=f"Customer created:\n\tName: {name}, Dni: {dni}, Phone number: {phone_number}, Addres: {address}, Email{email}")
        message.save()
        return super().form_valid(form)


class ReadDataListView(LoginRequiredMixin, ListView):
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
    """
    Displays a list of data types and their associated information.
    
    It inherits from the ListView class and requires the user to be logged in.
    
    Methods:
        get_context_data: overrides the parent class method to add additional context data to the view such as user-selected data types.
    """
    model = Customer
    template_name = 'customers_search_datatype.html'
    def get_queryset(self):
        datatype_input = self.request.GET["datatype_input"].strip()
        return get_customers_for_search_input(datatype_input,"")
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Overrides the get_context_data method of the parent class to add additional context data to the view.
        
        Retrieves the 'datatype_input' parameter from the GET parameters of the request, removes any leading or trailing whitespace,
        and updates the context with the result of the 'get_context_for_search_input_in_customers_section' function with the data needed to populate the view with the chosen datatypes.
            
        Returns:
            A dictionary containing the context data for the view.
        """
        context = super().get_context_data(**kwargs)
        datatype_input = self.request.GET["datatype_input"].strip()
        context.update(get_context_for_datatype_input_in_customers_section(datatype_input))
        return context

class NameCheckView(LoginRequiredMixin,TemplateView):
    template_name = 'answer_customer_name.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
class DniCheckView(LoginRequiredMixin,TemplateView):
    template_name = 'answer_customer_dni.html'
class PhoneNumberCheckView(LoginRequiredMixin,TemplateView):
    template_name = 'answer_customer_phone_number.html'
class AddressCheckView(LoginRequiredMixin,TemplateView):
    template_name = 'answer_customer_address.html'
class EmailCheckView(LoginRequiredMixin,TemplateView):
    template_name = 'answer_customer_email.html'
class CreateConfirmView(LoginRequiredMixin,TemplateView):#Esta clase no creo que pueda ser un template view porque debe manejar una solicitud post
    template_name = 'template.html'
