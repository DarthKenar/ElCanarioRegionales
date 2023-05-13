# from django.shortcuts import get_object_or_404
# from articles.models import Categories, Colors, Sizes, Materials
from typing import Tuple
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Value, ArticleValue
import re
@login_required
def render_login_required(request, template: str,context: dict): 
    """This function is used for all functions that require the user to be logged in."""

    return render(request, template, context)

def value_in_context_is_empty(QuerySet:any)-> bool:
    """Checks if the QuerySet is empty or not, returning True if it is empty and False if it has one or more elements inside."""

    quantity = QuerySet.count()
    if quantity < 1:
        return True
    else:
        return False
    
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
    
def name_check(article_name_input:str)->dict:
    """checks that the name meets the following conditions:
        -is not empty
        -not alphanumeric
    in these cases returns a response that is added to the context to be used by another function.
    if no errors are found then an empty string is returned as answer.
    """

    if article_name_input == '':

        context = {"answer_error_name": "Este campo es obligatorio"}
        
    elif not article_name_input.isalpha():
        
        context = {"answer_error_name": "El nombre del artículo no debe contener números, simbolos o espacios."}
    
    else:
        
        context = {"answer_error_name": ""}
    
    return context
def calculator_check(increase: str, buy_price: str, context: dict) -> Tuple[dict, bool]:
    """
        - Receives the buy price* and increase*
        - Check these for errors (such as being empty or containing letters).
        - Returns a tuple with: (dict, boolean)
            - dict: error responses
            - boolean: If there is an error, true, otherwise false.
    """

    error_any = False
    if string_is_empty(increase) or string_is_empty(buy_price):

        error_any = True
        context["answer_empty_error"] = "Debes completar los campos para calcular el precio de venta"

    if not buy_price.replace(".","0",1).isnumeric() or  not increase.replace(".","0",1).isnumeric():
        error_any = True
        context["answer_string_error"] = "Los datos ingresados deben ser numéricos"

    return context, error_any
def search_any_error_in_name_field(name_input:str,context: dict) -> Tuple[dict,bool]:
    """check that no errors are found for the name field.
    returns:
        1- boolean: If one error is founded returns True else, False
        2- dictionary: The error answers if one of them is founded
        """
    any_error = False

    if name_input == "":
        any_error = True
        context['answer_error_name'] = 'Es obligatorio completar el nombre.'
    elif not name_input.isalpha():
        any_error = True
        context['answer_error_name'] = 'El nombre no debe contener números, simbolos o espacios.'

    return(context, any_error)


def get_values_for_categories(request: object) -> dict:
    """
    It obtains the selected values and saves them in a dictionary in which the structure is as follows:
    dict={'category.id': 'value_id'}
    Note the difference between calling the id attribute for the category and storing the instance of value as value
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


    has_internal_spaces = bool(re.search(r'\S\s+\S', name))
    if has_internal_spaces:
        context['answer_error_name'] = "El nombre no debe contener espacios."
    return context, has_internal_spaces

def name_already_in_db(name:str, Model:object, context:dict) -> Tuple[dict,bool]:
    """Returns the answer in a dictionary (updating it) and True in case the entered name is found in the database"""

    print("name already in db? --> checking...")
    any_error = False
    query = Model.objects.all()
    name = name.strip().title()
    for obj in query:
        if obj.name == name:
            print(f" TRUE - name {name} is already in db!")
            any_error = True
            context["answer_error_name"] = f"El nombre {name} ya existe!"
    
    return context, any_error

def is_empty_name(s: str, context: dict) -> Tuple[dict, bool]:
    """Returns True if the string is empty or contains only blanks."""
    
    
    any_error =  string_is_empty(s)
    if any_error == True:
        context['answer_error_name'] = 'Es obligatorio completar el nombre.'
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