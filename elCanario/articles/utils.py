# from django.shortcuts import get_object_or_404
# from articles.models import Categories, Colors, Sizes, Materials
# from typing import Tuple
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def render_login_required(request, template: str,context: dict): 
    """
    This function is used for all functions that require the user to be logged in.
    """

    return render(request, template, context)
def value_in_context_is_empty(QuerySet:any)-> bool:
    """Checks if the QuerySet is empty or not, returning True if it is empty and False if it has one or more elements inside."""
    quantity = QuerySet.count()
    print(quantity)
    if quantity < 1:
        return True
    else:
        return False
def is_empty(s):
    """
    Returns True if the string is empty or contains only blanks.
    """
    return s is None or s.strip() == ''
# def title(title: str)->str:
#     """get a string title and returns the first letter of the word in upper case and the others in lower case"""
#     try:
#         return title.title()
#     except(TypeError, ValueError):
#         return title
    
# def articles_create_confirm_get_category(input: int) -> object:
#     """retrieves an id(int) and returns the object corresponding to that id"""

#     category_object = get_object_or_404(Categories, id = input)
#     return category_object

# def articles_create_confirm_get_color(input: int) -> object:
#     """retrieves an id(int) and returns the object corresponding to that id"""

#     color_object = get_object_or_404(Colors, id = input)
#     return color_object

# def articles_create_confirm_get_material(input: int) -> object:
#     """retrieves an id(int) and returns the object corresponding to that id"""

#     material_object = get_object_or_404(Materials, id = input)
#     return material_object

# def articles_create_confirm_get_size(input: int) -> object:
#     """retrieves an id(int) and returns the object corresponding to that id"""

#     size_object = get_object_or_404(Sizes, id = input)
#     return size_object

# def str_to_int_if_possible(input:str):
#     """converts a string to an integer if possible"""

#     if input.isnumeric():
#         input = int(input)

#     return input

# def name_check(article_name_input:str)->dict:
#     """checks that the name meets the following conditions:
#         -is not empty
#         -not alphanumeric
#     in these cases returns a response that is added to the context to be used by another function.
#     if no errors are found then an empty string is returned.
#     """

#     if article_name_input == '':

#         context = {"answer_article_name": "Este campo es obligatorio"}
        
#     elif not article_name_input.isalpha():
        
#         context = {"answer_article_name": "El nombre del artículo no debe contener números, simbolos o espacios."}
    
#     else:
        
#         context = {"answer_article_name": ""}
    
#     return context
        
# def category_check(article_category_input:str, context:dict)->dict:
#     """checks that the category is not empty.
#     If it is empty then it adds a new error response to the context to be used by another function.
#     If the category is selected then it returns the error response as an empty string."""

#     if article_category_input == 'Empty':

#         context["answer_category_id"] = "Es obligatorio seleccionar una categoría."
    
#     else:
#         context["answer_category_id"] = ""

#     return context

# def search_any_error(name_input:str, category_input:str, sell_price:str, context: dict) -> Tuple[bool,dict]:
#     """check that no errors are found for the fields "name", "category" and "sell_price".
#     returns two objects:
#         1- boolean: If one error is founded returns True else, False
#         2- dictionary: The error answers if one of them is founded
         
#     """

#     any_error = False

#     if name_input == "":
#         any_error = True
#         context['answer_article_name'] = 'Es obligatorio completar el nombre.'
#     elif not name_input.isalpha():
#         any_error = True
#         context['answer_article_name'] = 'El nombre del artículo no debe contener números, simbolos o espacios.'

#     if category_input == 'Empty':
#         any_error = True
#         context['answer_category_id'] = 'Es obligatorio seleccionar una categoría.'
    

#     try:
#         float(sell_price.replace(",",".",1))
#     except:

#         any_error = True
#         context['answer_sell_price'] = "Porfavor, calcule correctamente el precio de venta."

#     return(any_error, context)

# def get_objects(article_category_input: str,article_color_input: str,article_material_input:str,article_size_input: str)->dict:
#     """receives four ids(str) as a string and returns a dictionary containing the retrieved objects:
#         -category
#         -color
#         -material
#         -size
#     """
#     if article_category_input != 'Empty':

#         article_category_input= int(article_category_input)
#         article_category_object = articles_create_confirm_get_category(article_category_input)

#     if article_color_input != 'Empty':

#         article_color_input = int(article_color_input)
#         article_color_object = articles_create_confirm_get_color(article_color_input)

#     else:

#         article_color_object = None

#     if article_material_input != 'Empty':

#         article_material_input = int(article_material_input)
#         article_material_object = articles_create_confirm_get_material(article_material_input)

#     else:

#         article_material_object = None

#     if article_size_input != 'Empty':

#         article_size_input = int(article_size_input)
#         article_size_object = articles_create_confirm_get_size(article_size_input)

#     else:

#         article_size_object = None

#     objects = {"article_category_object":article_category_object,
#                "article_color_object":article_color_object,
#                "article_material_object":article_material_object,
#                "article_size_object":article_size_object
#                }
#     return objects
