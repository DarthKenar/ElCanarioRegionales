# from django.shortcuts import get_object_or_404
# from articles.models import Categories, Colors, Sizes, Materials
from typing import Tuple
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Value, ArticleValue, Article, Customer
import re
@login_required
def render_login_required(request, template: str,context: dict): 
    """This function is used for all functions that require the user to be logged in."""

    return render(request, template, context)

# def value_in_context_is_empty(QuerySet:any)-> bool:
#     """Checks if the QuerySet is empty or not, returning True if it is empty and False if it has one or more elements inside."""

#     quantity = QuerySet.count()
#     if quantity < 1:
#         return True
#     else:
#         return False
    
def string_is_empty(s):
    """Returns True if the string is empty or contains only blanks."""
    print("Its empty name? --> checking...")
    return s is None or s.strip() == ''

def title(title: str)->str:
    """get a string title and returns the first letter of the word in upper case and the others in lower case"""
    try:
        return title.title()
    except(TypeError, ValueError):
        return title

def calculator_check(increase: str, buy_price: str, context: dict) -> Tuple[dict, bool]:
    """Check if they contain errors such as being empty or containing letters. The increase and buyprice fields must be numeric.

    Args:
        increase (str): percentage increase received as string
        buy_price (str): buy price received as string
        context (dict): the context for renaming the value of the key used as a response to the user is received

    Returns:
        Tuple[dict, bool]: returns in the first position the context and in the second position the boolean answer
    """

    error_any = False
    if string_is_empty(increase) or string_is_empty(buy_price):

        error_any = True
        context["answer_empty_error"] = "You must fill in the fields to calculate the selling price."

    if not buy_price.replace(".","0",1).isnumeric() or  not increase.replace(".","0",1).isnumeric():
        error_any = True
        context["answer_string_error"] = "The data entered must be numeric"

    return context, error_any
def search_any_error_in_name_field(name_input:str, context: dict) -> Tuple[dict,bool]:
    """checks that it is not an empty string and checks that it is not different from an alphanumeric string

    Args:
        name_input (str): name to check
        context (dict): the context for renaming the value of the key used as a response to the user is received

    Returns:
        Tuple[dict,bool]: returns in the first position the context and in the second position the boolean answer
    """
    any_error = False

    if name_input == "":
        any_error = True
        context['answer_error_name'] = 'It is mandatory to fill in the name.'
    elif not name_input.isalpha():
        any_error = True
        context['answer_error_name'] = 'The name must not contain numbers, symbols or spaces.'

    return(context, any_error)


def get_values_for_categories(request: object) -> dict:
    print(request)
    """Gets the values selected for each of the categories (used to store the values of each category of an article being created) and saves them in a dictionary whose structure is as follows

        dict={'category.id': 'value_id'}

        The dictionary can be used to return in context the chosen categories and their respective values

    Args:
        request (object): the object to be received is the request with all the values selected for the existing categories

    Returns:
        dict: 
            dict={'category.id': 'value_id'}
            - all categories and selected values
    """

    categories = Category.objects.all()
    values_dict = {}
    for category in categories:
        
        if request.GET['category-'+str(category.id)] != '':
            values_dict[str(category.id)]= Value.objects.get(id = int(request.GET['category-'+str(category.id)]))
        else:
            values_dict[str(category.id)]= None

    return values_dict

def string_has_internal_spaces(name:str, context) -> Tuple[dict,bool]:
    """check that the string has spaces

    Args:
        name (str): name or string to check
        context (_type_): the context for renaming the value of the key used as a response to the user is received

    Returns:
        Tuple[dict,bool]: returns in the first position the context and in the second position the boolean answer
    """

    has_internal_spaces = bool(re.search(r'\S\s+\S', name))
    if has_internal_spaces:
        context['answer_error_name'] = "The name must not contain spaces."
    return context, has_internal_spaces

def name_already_in_db(name:str, Model:object, context:dict) -> Tuple[dict,bool]:
    """Returns the answer in a dictionary (updating it) and True in case the entered name is found in the database

    Args:
        name (str): name to check
        Model (object): database model in which the name is searched
        context (dict): the context for renaming the value of the key used as a response to the user is received

    Returns:
        Tuple[dict,bool]: returns in the first position the context and in the second position the boolean answer
    """

    print("name already in db? --> checking...")
    any_error = False
    query = Model.objects.all()
    name = name.strip().title()
    for obj in query:
        if obj.name == name:
            print(f" TRUE - name {name} is already in db!")
            any_error = True
            context["answer_error_name"] = f"The name {name} already exists!"
        
    return context, any_error

def is_empty_name(s: str, context: dict) -> Tuple[dict, bool]:
    """Returns True if the string is empty or contains only blanks.


    Args:
        s (str): string to check
        context (dict): the context for renaming the value of the key used as a response to the user is received
    Returns:
        Tuple[dict, bool]: returns in the first position the context and in the second position the boolean answer
    """
    
    
    any_error =  string_is_empty(s)
    if any_error == True:
        context['answer_error_name'] = 'Complete the name is obligatory.'
    return context, any_error

def delete_old_values(article):
    "removes the values related to an article, this function is used to re-record the new values that an article has in articles_update."
    query = ArticleValue.objects.filter(article_id = article.id)
    for obj in query:
        obj.delete()

def str_to_bool_external_link(external_link: str) -> bool:
    """gets a string as 'True' or 'False' and converts it to Boolean returning this value"""
    if external_link == 'True':
        external_link = True
    else:
        external_link = False
    return external_link

def is_the_same_name(new_name:str, old_name:str, context: dict) -> Tuple[dict, bool]:
    any_error = False
    if new_name.strip().title() == old_name.strip().title():
        any_error = True
        context.update({
            'answer_error_name': 'The old name and the new name are the same'
        })
    return context, any_error

def get_articles_by_category_datatype(datatype_input: str) -> dict:

    context = {}

    datatype_input = int(datatype_input)
    category = Category.objects.get(id = datatype_input)

    context.update({
        "datatype_input": category.id,
        "datatype": category.name,
        "articles_any": Article.objects.filter(characteristics_id__category_id=category),
        "values": Value.objects.filter(category_id=category)
    })

    return context

def get_articles_by_native_datatype(datatype_input: str) -> dict:

    context = {}

    datatype_dict = {
                    1: "id",
                    2: "name",
                    3: "buy_price",
                    4: "increase",
                    5: "sell_price"
                    }
    
    articles = Article.objects.all()

    context.update({
        "datatype_input": datatype_input,
        "articles_any": articles
    })
    
    if datatype_input == datatype_dict[1]:

        context["datatype_input"] = datatype_input
        context["datatype"] = "Id"

    elif datatype_input == datatype_dict[2]:

        context["datatype"] = "Name"
        
    elif datatype_input == datatype_dict[3]:

        context["datatype"] = "Buy price"

    elif datatype_input == datatype_dict[4]:

        context["datatype"] = "Increment"

    else: #datatype_input == datatype_dict[5]

        context["datatype_input"] = datatype_input
        context["datatype"] = "Sell price"
    
    return context

def get_customers_by_native_datatype(datatype_input: str) -> dict:
    context = {}
    datatype_dict = {
                    1: "id",
                    2: "name",
                    3: "phone_number",
                    4: "email",
                    5: "address"
                    }
    
    customers = Customer.objects.all()

    context.update({
        "datatype_input": datatype_input,
        "customers_any": customers
    })

    if datatype_input == datatype_dict[1]:

        context["datatype_input"] = datatype_input
        context["datatype"] = "Id"

    elif datatype_input == datatype_dict[2]:

        context["datatype"] = "Nombre"
        
    elif datatype_input == datatype_dict[3]:

        context["datatype"] = "Teléfono"

    elif datatype_input == datatype_dict[4]:

        context["datatype"] = "E-mail"

    else: #datatype_input == datatype_dict[5]

        context["datatype_input"] = datatype_input
        context["datatype"] = "Dirección"

    return context

def get_articles_for_value_of_category(datatype_input: str,search_input: str) -> dict:
        
        context = {}
        datatype_input = int(datatype_input)
        search_input = int(search_input)

        category = Category.objects.get(id = datatype_input)
        value = Value.objects.get(id = search_input)
        context["articles_any"] = Article.objects.filter(characteristics_id=value)
        context["datatype_input"] = category.id
        context["datatype"] = category.name
        context["value"] = value.name

        return context
def get_articles_for_search_input_in_native_datatype(datatype_input:str, search_input:str) -> dict:

    context = {}
    context["value"] = search_input

    if datatype_input == "id":
        context["articles_any"] = Article.objects.filter(id__startswith=search_input)
        context["datatype_input"] = "id"
        context["datatype"] = "Id:"
    elif datatype_input == "name":
        context["articles_any"] = Article.objects.filter(name__startswith=search_input) 
        context["datatype_input"] = "name"
        context["datatype"] = "Nombre:"
    elif datatype_input == "buy_price":
        context["articles_any"] = Article.objects.filter(buy_price__startswith=search_input)
        context["datatype_input"] = "buy_price"
        context["datatype"] = "Precio de compra:"
    elif datatype_input == "increase":
        context["articles_any"] = Article.objects.filter(increase__startswith=search_input)
        context["datatype_input"] = "increase"
        context["datatype"] = "Incremento:"
    elif datatype_input == "sell_price":
        context["articles_any"] = Article.objects.filter(sell_price__startswith=search_input)
        context["datatype_input"] = "sell_price"
        context["datatype"] = "Precio de venta:"

    return context

def get_customers_for_search_input_in_native_datatype(datatype_input:str, search_input:str) -> dict:

    context = {}
    context["value"] = search_input

    if datatype_input == "id":
        context["customers_any"] = Article.objects.filter(id__startswith=search_input)
        context["datatype_input"] = "id"
        context["datatype"] = "Id:"
    elif datatype_input == "address":
        context["customers_any"] = Article.objects.filter(address__startswith=search_input) 
        context["datatype_input"] = "address"
        context["datatype"] = "Dirección:"
    elif datatype_input == "email":
        context["customers_any"] = Article.objects.filter(email__startswith=search_input)
        context["datatype_input"] = "email"
        context["datatype"] = "Email:"
    elif datatype_input == "name":
        context["customers_any"] = Article.objects.filter(name__startswith=search_input)
        context["datatype_input"] = "name"
        context["datatype"] = "Nombre:"
    elif datatype_input == "phone_number":
        context["customers_any"] = Article.objects.filter(phone_number__startswith=search_input)
        context["datatype_input"] = "phone_number"
        context["datatype"] = "Numero de teléfono:"
def keep_selected_values(request)->dict:
    print(type(request))
    """
    received: request
    returns: dictionary
    returns a dictionary containing a list in the key 'selected_values' with the ids of the selected values. 
    It is used to keep the selected values when trying to create an article."""
    values_selected:list = []
    categories = Category.objects.all()

    for category in categories:
        
        if not request.GET[f"category-{category.id}"] == "":
            values_selected.append(int(request.GET[f"category-{category.id}"]))

    return {"values_selected":values_selected}
