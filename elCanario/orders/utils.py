from decimal import Decimal
from customers.models import Customer
from orders.models import Order
from articles.models import Article
from typing import Dict
from django.utils.translation import gettext_lazy as _
from elCanario.utils import string_is_empty
from django.utils import timezone
from datetime import datetime
from orders.models import Order
from customers.models import Customer
import pytz
def get_orders_for_search_input(datatype_input:str, search_input:str=''):
    """Filters orders depending on the type of search entered by the user

    Args:
        datatype_input (str): Type of data entered by the user
        search_input (str, optional): Specific data entered by the user. Defaults to ''.

    Returns:
        Query_set: List of filtered orders
    """
    if string_is_empty(search_input):
        return Order.objects.all()
    if datatype_input == "id":
        return Order.objects.filter(id__startswith=search_input)
    elif datatype_input == "customer_id":
        return Order.objects.filter(customer_id=search_input) 
    elif datatype_input == "articles_cart":
        return Order.objects.filter(articles_cart=search_input)
    elif datatype_input == "article_quantity":
        return Order.objects.filter(article_quantity__startswith=search_input)
    elif datatype_input == "total_pay":
        return Order.objects.filter(total_pay__startswith=search_input)
    elif datatype_input == "details":
        return Order.objects.filter(details__startswith=search_input)
    elif datatype_input == "creation_date":
        #https://docs.djangoproject.com/en/4.2/ref/models/querysets/#dates
        date_input = timezone.make_aware(datetime.strptime(search_input, '%Y-%m-%d'))
        return Order.objects.filter(creation_date__date=date_input)
    elif datatype_input == "updated_date":
        return Order.objects.filter(updated_date__date=search_input)
    else:# datatype_input == "delivery_status":
        if search_input == 'None':
            search_input = None # type: ignore
        return Order.objects.filter(delivery_status=search_input)
    
def get_context_for_search_input_in_orders_section(datatype_input:str, search_input:str) -> Dict[str,str]:
    """gets the contextual answers that correspond to the value set for the user.

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
        context["datatype"] = _("ID")
    elif datatype_input == "customer_id":
        context["datatype_input"] = "customer_id"
        context["datatype"] = _("Customer")
    elif datatype_input == "articles_cart":
        context["datatype_input"] = "articles_cart"
        context["datatype"] = _("Article/s")
    elif datatype_input == "article_quantity":
        context["datatype_input"] = "article_quantity"
        context["datatype"] = _("Articles quantity")
    elif datatype_input == "total_pay":
        context["datatype_input"] = "total_pay"
        context["datatype"] = _("Total pay")
    elif datatype_input == "details":
        context["datatype_input"] = "details"
        context["datatype"] = _("Details")
    elif datatype_input == "creation_date":
        context["datatype_input"] = "creation_date"
        context["datatype"] = _("Creation date")
    elif datatype_input == "updated_date":
        context["datatype_input"] = "updated_date"
        context["datatype"] = _("Updated date")
    else:# datatype_input == "delivery_status":
        context["datatype_input"] = "delivery_status"
        context["datatype"] = _("Delivery Status")
    return context

def get_context_for_datatype_input_in_orders_section(datatype_input:str):
    """gets the contextual answers that correspond to the value set in the selected native data type.

    Native data type is understood as attributes of the orders model.
    
    Args:
        datatype_input (str): corresponds to the data type to search for.
        search_input (str): corresponds to the value to search according to datatype_input.

    Returns:
        dict: returns the values that will be needed in the context dictionary, are selected datatypes, filtered orders, list of datatypes to select
    """
    context = {}
    context["datatype_input"] = datatype_input
    if datatype_input == "id":
        context["datatype_input"] = "id"
        context["datatype"] = _("ID")
    elif datatype_input == "customer_id":
        context["datatype_input"] = "customer_id"
        context["datatype"] = _("Customer")
        context["customer_list"] = Customer.objects.all()
    elif datatype_input == "articles_cart":
        context["datatype_input"] = "articles_cart"
        context["datatype"] = _("Article/s")
        context["article_list"] = Article.objects.all()
    elif datatype_input == "article_quantity":
        context["datatype_input"] = "article_quantity"
        context["datatype"] = _("Articles quantity")
    elif datatype_input == "total_pay":
        context["datatype_input"] = "total_pay"
        context["datatype"] = _("Total pay")
    elif datatype_input == "details":
        context["datatype_input"] = "details"
        context["datatype"] = _("Details")
    elif datatype_input == "creation_date":
        context["datatype_input"] = "creation_date"
        context["datatype"] = _("Creation date")
    elif datatype_input == "updated_date":
        context["datatype_input"] = "updated_date"
        context["datatype"] = _("Updated date")
    else:# datatype_input == "delivery_status":
        context["datatype_input"] = "delivery_status"
        context["datatype"] = _("Delivery Status")
    return context

def update_article_quantity(order):
    """Update the quantity of items in the order

    Args:
        order (Order): Receives an object of type order to modify its article_quantity attribute
    """
    article_count  = order.articles_cart.count()
    order.article_quantity = article_count
    order.save()

def update_total_pay(order):
    """Update the total pay in the order

    Args:
        order (Order): Receives an object of type order to modify its total_pay attribute
    """
    total_pay = Decimal(0)
    for articles in order.articles_cart.all():
        total_pay += articles.sell_price
    order.total_pay = total_pay
    order.save()

def update_total_purchased(order):
    """Update the total purchased in the order (total sum of the price of the articles included in the order)

    Args:
        order (Order): Receives an object of type order to modify its total_purchased attribute
    """
    customer = Customer.objects.get(id = order.customer_id.id)
    order_list_for_customer = Order.objects.filter(customer_id = customer)
    total = Decimal(0)
    for order in order_list_for_customer:
        if order.delivery_status == True:
            total = total + order.total_pay
    customer.total_purchased = total
    customer.save()
    