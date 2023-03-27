from django.shortcuts import get_object_or_404
from articles.models import Categories, Colors, Sizes, Materials

def is_empty(s):
    """
    Returns True if the string is empty or contains only blanks.
    """
    return s is None or s.strip() == ''

def articles_create_confirm_get_category(input: int) -> object:
    category_object = get_object_or_404(Categories, id = input)
    return category_object
def articles_create_confirm_get_color(input: int) -> object:
    color_object = get_object_or_404(Colors, id = input)
    return color_object
def articles_create_confirm_get_material(input: int) -> object:
    material_object = get_object_or_404(Materials, id = input)
    return material_object
def articles_create_confirm_get_size(input: int) -> object:
    size_object = get_object_or_404(Sizes, id = input)
    return size_object

def str_to_int_if_possible(input:str):

    if input.isnumeric():
        input = int(input)

    return input

def name_check(article_name_input:str)->dict:

    if article_name_input == '':

        context = {"answer_article_name": "Este campo es obligatorio"}
        
    elif not article_name_input.isalpha():
        
        context = {"answer_article_name": "El nombre del artículo no debe contener números, simbolos o espacios."}
    
    else:
        
        context = {"answer_article_name": ""}
    
    return context
        
def category_check(article_category_input:str, context:dict)->dict:

    if article_category_input == 'Empty':

        context["answer_category_id"] = "Es obligatorio seleccionar una categoría."
    
    else:
        context["answer_category_id"] = ""

    return context

def search_any_error(name_input:str, category_input:str, sell_price:str, context: dict) -> bool:

    any_error = False

    if name_input == "":
        any_error = True
        context['answer_article_name'] = 'Es obligatorio completar el nombre.'
    elif not name_input.isalpha():
        any_error = True
        context['answer_article_name'] = 'El nombre del artículo no debe contener números, simbolos o espacios.'

    if category_input == 'Empty':
        any_error = True
        context['answer_category_id'] = 'Es obligatorio seleccionar una categoría.'
    

    try:
        float(sell_price.replace(",",".",1))
    except:

        any_error = True
        context['answer_sell_price'] = "No se puede calcular correctamente el precio de venta."

    return(any_error, context)

def get_objects(article_category_input: str,article_color_input: str,article_material_input:str,article_size_input: str)->dict:

    if article_category_input != 'Empty':

        article_category_input= int(article_category_input)
        article_category_object = articles_create_confirm_get_category(article_category_input)

    if article_color_input != 'Empty':

        article_color_input = int(article_color_input)
        article_color_object = articles_create_confirm_get_color(article_color_input)

    else:

        article_color_object = None

    if article_material_input != 'Empty':

        article_material_input = int(article_material_input)
        article_material_object = articles_create_confirm_get_material(article_material_input)

    else:

        article_material_object = None

    if article_size_input != 'Empty':

        articles_create_confirm_get_size = int(articles_create_confirm_get_size)
        article_size_object = articles_create_confirm_get_size(article_size_input)

    else:

        article_size_object = None

    objects = {"article_category_object":article_category_object,
               "article_color_object":article_color_object,
               "article_material_object":article_material_object,
               "article_size_object":article_size_object
               }
    return objects
