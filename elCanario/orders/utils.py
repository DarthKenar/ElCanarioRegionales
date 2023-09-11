from customers.models import Customer
from orders.models import Order
from typing import Dict
from elCanario.utils import string_is_empty
def get_orders_for_search_input(datatype_input:str, search_input:str=''):
    if string_is_empty(search_input):
        return Order.objects.all()
    if datatype_input == "id":
        return Order.objects.filter(id__startswith=search_input)
    elif datatype_input == "customer_id":
        return Order.objects.filter(customer_id=search_input) 
    elif datatype_input == "articles_cart":
        return Order.objects.filter(articles_cart__startswith=search_input)
    elif datatype_input == "article_quantity":
        return Order.objects.filter(article_quantity__startswith=search_input)
    elif datatype_input == "total_pay":
        return Order.objects.filter(total_pay__startswith=search_input)
    elif datatype_input == "details":
        return Order.objects.filter(details__startswith=search_input)
    elif datatype_input == "creation_date":
        return Order.objects.filter(creation_date__startswith=search_input)
    elif datatype_input == "updated_date":
        return Order.objects.filter(updated_date__startswith=search_input)
    else:# datatype_input == "delivery_status":
        if search_input == 'None':
            search_input = None # type: ignore
        return Order.objects.filter(delivery_status=search_input)
    
def get_context_for_search_input_in_orders_section(datatype_input:str, search_input:str) -> Dict[str,str]:
    """gets the orders that correspond to the value set in the selected native data type.

    Native data type is understood as attributes of the orders model.
    
    Args:
        datatype_input (str): corresponds to the data type to search for.
        search_input (str): corresponds to the value to search according to datatype_input.

    Returns:
        dict: returns the values that will be needed in the context dictionary, are selected datatypes, filtered orders, list of datatypes to select
    """
    context = {}
    context["value"] = search_input
    context["datatype_input"] = datatype_input
    if datatype_input == "id":
        context["datatype_input"] = "id"
        context["datatype"] = "ID"
    elif datatype_input == "customer_id":
        context["datatype_input"] = "customer_id"
        context["datatype"] = "Customer"
    elif datatype_input == "articles_cart":
        context["datatype_input"] = "articles_cart"
        context["datatype"] = "Article/s"
    elif datatype_input == "article_quantity":
        context["datatype_input"] = "article_quantity"
        context["datatype"] = "Articles quantity"
    elif datatype_input == "total_pay":
        context["datatype_input"] = "total_pay"
        context["datatype"] = "Total pay"
    elif datatype_input == "details":
        context["datatype_input"] = "details"
        context["datatype"] = "Details"
    elif datatype_input == "creation_date":
        context["datatype_input"] = "creation_date"
        context["datatype"] = "Creation date"
    elif datatype_input == "updated_date":
        context["datatype_input"] = "updated_date"
        context["datatype"] = "Updated date"
    else:# datatype_input == "delivery_status":
        context["datatype_input"] = "delivery_status"
        context["datatype"] = "Delivery Status"
    return context

def get_context_for_datatype_input_in_orders_section(datatype_input:str):
    context = {}
    context["datatype_input"] = datatype_input
    if datatype_input == "id":
        context["datatype_input"] = "id"
        context["datatype"] = "ID"
    elif datatype_input == "customer_id":
        context["datatype_input"] = "customer_id"
        context["datatype"] = "Customer"
        context["customer_list"] = Customer.objects.all()
    elif datatype_input == "articles_cart":
        context["datatype_input"] = "articles_cart"
        context["datatype"] = "Article/s"
    elif datatype_input == "article_quantity":
        context["datatype_input"] = "article_quantity"
        context["datatype"] = "Articles quantity"
    elif datatype_input == "total_pay":
        context["datatype_input"] = "total_pay"
        context["datatype"] = "Total pay"
    elif datatype_input == "details":
        context["datatype_input"] = "details"
        context["datatype"] = "Details"
    elif datatype_input == "creation_date":
        context["datatype_input"] = "creation_date"
        context["datatype"] = "Creation date"
    elif datatype_input == "updated_date":
        context["datatype_input"] = "updated_date"
        context["datatype"] = "Updated date"
    else:# datatype_input == "delivery_status":
        context["datatype_input"] = "delivery_status"
        context["datatype"] = "Delivery Status"
    return context