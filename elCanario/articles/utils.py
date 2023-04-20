# from django.shortcuts import get_object_or_404
# from articles.models import Categories, Colors, Sizes, Materials
from typing import Tuple
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Value
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
    
def is_empty(s):
    """Returns True if the string is empty or contains only blanks."""

    return s is None or s.strip() == ''

def title(title: str)->str:
    """get a string title and returns the first letter of the word in upper case and the others in lower case"""
    try:
        return title.title()
    except(TypeError, ValueError):
        return title
    

# def str_to_int_if_possible(input:str):
#     """converts a string to an integer if possible"""

#     if input.isnumeric():
#         input = int(input)

#     return input

def name_check(article_name_input:str)->dict:
    """checks that the name meets the following conditions:
        -is not empty
        -not alphanumeric
    in these cases returns a response that is added to the context to be used by another function.
    if no errors are found then an empty string is returned.
    """

    if article_name_input == '':

        context = {"answer_article_name": "Este campo es obligatorio"}
        
    elif not article_name_input.isalpha():
        
        context = {"answer_article_name": "El nombre del artículo no debe contener números, simbolos o espacios."}
    
    else:
        
        context = {"answer_article_name": ""}
    
    return context
def calculator_check(increase: str, buy_price: str) -> Tuple[dict, bool]:
    """
        - Receives the buy price* and increase*
        - Check these for errors (such as being empty or containing letters).
        - Returns a tuple with: (dict, boolean)
            - dict: error responses
            - boolean: If there is an error, true, otherwise false.
    """
    context = {}
    error_any = False
    if is_empty(increase) or is_empty(buy_price):

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

def search_any_error(name_input:str, sell_price:str, context: dict) -> Tuple[dict,bool]:
    """check that no errors are found for the fields "name" and "sell_price".
    returns:
        1- boolean: If one error is founded returns True else, False
        2- dictionary: The error answers if one of them is founded
         
    """

    any_error = False
    search_any_error_in_name_field(name_input, context)

    try:
        float(sell_price.replace(",",".",1))
    except:

        any_error = True
        context['answer_sell_price'] = "Porfavor, calcule correctamente el precio de venta."

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

#AUTO GENERATE fields
from .models import Article, Category, Value, ArticleValue
import random


def generate_articles(num):
    names = ["co", "la","fla","men","pri","pro","sul","so","fa","ar","si","lla","fre","ir","gas","dor","mir","cro","no","va","ri","ta"]
    for _ in range(num):
        article = Article(
            name = f"{random.choice(names)}" + f"{random.choice(names)}" + f"{random.choice(names)}",
            buy_price = random.uniform(100, 500),
            increase = random.uniform(0,300),
        )
        article.sell_price = article.buy_price + ((article.buy_price * article.increase) / 100)

        try:
            article.save()
            
        except:
            num -= 1
            pass
    print(f"{num} articles generated correctly!")

def generate_categories_values(num_cat, num_val):
    names = ["Material", "Tipo", "Color", "Forma", "Tamaño", "Peso", "Marca", "Modelo", "Estilo", "Textura", "Sabor", "Olor", "Sonido", "Temperatura", "Dureza", "Flexibilidad", "Transparencia", "Brillo", "Elasticidad", "Resistencia", "Impermeabilidad", "Porosidad", "Adherencia", "Conductividad", "Reflectividad", "Refractividad", "Densidad", "Viscosidad", "Solubilidad","Fragilidad"]
    for _ in range(num_cat):
        category = Category(
            name = random.choice(names)
        )
        try:
            category.save()
        except:
            num_cat -= 1
            pass
        else:
            names = ["Algodón", "Seda", "Lana", "Cuero", "Madera", "Metal", "Plástico", "Vidrio", "Piedra", "Papel", "Zapato", "Camisa", "Pantalón", "Vestido", "Sombrero", "Guante", "Bufanda", "Corbata", "Rojo", "Azul", "Verde", "Amarillo", "Naranja", "Morado", "Negro", "Blanco", "Gris", "Marrón", "Rosa", "Beige","Circular","Cuadrado","Triangular","Rectangular","Hexagonal","Pequeño","Mediano","Grande","Ligero","Pesado","Nike","Adidas","Puma","Reebok","Under Armour","Levis","Calvin Klein","Tommy Hilfiger","Ralph Lauren","Lacoste","Moderno","Clásico","Vintage","Rústico","Urbano","Elegante","Casual","Deportivo","Suave","Áspero","Dulce","Salado","Amargo","Ácido","Picante","Umami","Floral","Cítrico","Herbáceo","Amaderado","Silencioso","Ruidoso","Musical"]
            for _ in range(num_val):

                value = Value(
                    category_id = category,
                    name = random.choice(names)
                )
                try:
                    value.save()
                except:
                    num_val -= 1
                    pass
        print(f"{num_val} values for {category.name} generated correctly!")
    print(f"{num_cat} categories generated correctly!") 

def generate_category_values_for_articles(num):
    values = Value.objects.all()
    articles = Article.objects.all()
    for _ in range(num):
        value_choiced = random.choice(values)
        article_value = ArticleValue(
            category_id = value_choiced.category_id,
            value_id = value_choiced,
            article_id = random.choice(articles)
        )
        
        try:
            article_value.save()
        except:
            num -= 1
            pass
    print(f"{num} relations category values for articles")

def generate(num):
    generate_articles(num*2)
    generate_categories_values(num,round(num/2))
    generate_category_values_for_articles(num*20)
