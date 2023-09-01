from msilib.schema import CustomAction
from typing import Tuple, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from articles.models import Category, Value, ArticleValue, Article
from customers.models import Customer
import re
from elCanario.utils import string_is_empty
def get_customers_for_search_input(datatype_input:str, search_input:str) -> object:
    if string_is_empty(search_input):
        return Customer.objects.all()
    if datatype_input == "id":
        return Customer.objects.filter(id__startswith=search_input)
    elif datatype_input == "name":
        return Customer.objects.filter(name__startswith=search_input) 
    elif datatype_input == "dni":
        return Customer.objects.filter(dni__startswith=search_input)
    elif datatype_input == "phone_number":
        return Customer.objects.filter(phone_number__startswith=search_input)
    elif datatype_input == "address":
        return Customer.objects.filter(address__startswith=search_input)
    elif datatype_input == "email":
        return Customer.objects.filter(email__startswith=search_input)
    else: #datatype_input == "total_purchased":
        return Customer.objects.filter(total_purchased__startswith=search_input)
    
def get_context_for_search_input_in_customers_section(datatype_input:str, search_input:str) -> Dict[str,str]:
    """gets the customers that correspond to the value set in the selected native data type.

    Native data type is understood as attributes of the customers model.
    
    Args:
        datatype_input (str): corresponds to the data type to search for.
        search_input (str): corresponds to the value to search according to datatype_input.

    Returns:
        dict: returns the values that will be needed in the context dictionary, are selected datatypes, filtered customers, list of datatypes to select
    """
    context = {}
    context["value"] = search_input
    context["datatype_input"] = datatype_input

    if datatype_input == "id":
        context["datatype_input"] = "id"
        context["datatype"] = "Id:"
    elif datatype_input == "address":
        context["datatype_input"] = "address"
        context["datatype"] = "Address:"
    elif datatype_input == "dni":
        context["datatype_input"] = "dni"
        context["datatype"] = "DNI:"
    elif datatype_input == "email":
        context["datatype_input"] = "email"
        context["datatype"] = "Email:"
    elif datatype_input == "name":
        context["datatype_input"] = "name"
        context["datatype"] = "Name:"
    elif datatype_input == "phone_number":
        context["datatype_input"] = "phone_number"
        context["datatype"] = "Phone number:"
    elif datatype_input == "total_purchased":
        context["datatype_input"] = "total_purchased"
        context["datatype"] = "Total purchased:"
    return context
