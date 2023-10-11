from mailbox import Message
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
from messageslog.models import MessageLog
from django.shortcuts import get_object_or_404
from customers.utils import get_context_for_search_input_in_customers_section, get_customers_for_search_input, get_context_for_datatype_input_in_customers_section
from elCanario.utils import render_login_required
# Create your views here.

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['datatype_input'] = 'name'
        context["datatype"] = _('Name')
        context["answer"] = "Customers in Database"
        return context


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers_create.html'
    success_url  = reverse_lazy('customers:customers')  

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.template_name = "create_form.html"
        return super().post(request, *args, **kwargs)
    
    def get_success_url(self) -> str:
        return reverse_lazy('customers:create_htmx') + '?correct'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        status = self.kwargs.get('status')
        if status == "True":
            name = form.cleaned_data['name']
            dni = form.cleaned_data['dni']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            message = MessageLog(info=f"Customer created:\n\tName: {name}, Dni: {dni}, Phone number: {phone_number}, Addres: {address}, Email{email}")
            message.save()
            return super().form_valid(form) #Esto hace que se guarde.
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
    def form_invalid(self, form):
        # Renderizar la plantilla con el formulario y los errores
        return self.render_to_response(self.get_context_data(form=form))


class CustomerCreateTemplate(LoginRequiredMixin,TemplateView):
    template_name = 'create_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CustomerForm()
        context['form'] = form
        return context


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


class CustomerUpdateTemplate(LoginRequiredMixin, TemplateView):
    template_name = "update_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objeto_id = self.kwargs.get('pk')
        object = get_object_or_404(Customer,id=objeto_id)
        print(object.name)
        context['object'] = object
        form = CustomerForm(instance=object) 
        context['form'] = form
        return context


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers_update.html"
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.template_name = "update_form.html"
        return super().post(request, *args, **kwargs)
    
    def get_success_url(self) -> str:
        return reverse_lazy('customers:update_htmx', args=[f"{self.object.id}"]) + '?correct'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        status = self.kwargs.get('status')
        if status == "True":
            name = form.cleaned_data['name']
            dni = form.cleaned_data['dni']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            message = MessageLog(info=f"Customer updated:\n\tName: {name}, Dni: {dni}, Phone number: {phone_number}, Addres: {address}, Email{email}")
            message.save()
            return super().form_valid(form) #Esto hace que se guarde.
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
    def form_invalid(self, form):
        # Renderizar la plantilla con el formulario y los errores
        return self.render_to_response(self.get_context_data(form=form))


@csrf_protect
def customer_delete(request:object, pk:int)-> HttpResponse:
    template = 'customers_search_data.html'
    context = {}
    try:
        customer = get_object_or_404(Customer, id=pk)
    except Exception as e:
        context["delete_answer"] = f"The selected item could not be deleted because it does not exist. Contact support."
        return render_login_required(request, template, context)
    else:
        context["delete_answer"] = f"Customer {customer.name} has been eliminated"
        message = MessageLog(info=f"Customer {customer.name} has been eliminated")
        message.save()
        customer.delete()
        articles = Customer.objects.all()
        context.update({"customer_list": articles,})
        return render_login_required(request, template, context)
