from django.shortcuts import render, get_object_or_404, redirect
from articles.models import Articles, Categories, Colors, Sizes, Materials
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .utils import *

# ORDERS SECTION
@login_required
def orders_deliver(request, template: str,context: dict): 
    """
    This function is used for all functions that require the user to be logged in.
    This function is used by all the Orders section functions that render a template.
    """

    return render(request, template, context)

def orders(request):
    return render(request, template_name="orders.html",context={})

# ARTICLES SECTION
@login_required
def articles_deliver(request, template: str,context: dict): 
    """
    This function is used for all functions that require the user to be logged in.
    This function is used by all the Articles section functions that render a template.
    """

    return render(request, template, context)

def articles(request):

    answer = "Artículos en la Base de datos"
    articles = Articles.objects.all()
    context = {"articles_all":articles,
               "articles_any": articles,
               "answer":answer}
    template = "articles.html"
    return articles_deliver(request, template, context)

### Articles read
def articles_read(request):

    datatype_dict = {
        0: "selection_empty",
        1: "id",
        2: "article_name",
        3: "category_id",
        4: "color_id",
        5: "material_id",
        6: "size_id",
        7: "buy_price",
        8: "increase",
        9: "sell_price"
    }

    datatype_input = request.GET['datatype_input']
    article_input = request.GET['article_input']

    if article_input:

        if datatype_input == datatype_dict[1]:
            datatype = "ID"
            articles = Articles.objects.filter(id__startswith=article_input)
        elif datatype_input == datatype_dict[2]:
            datatype = "Nombre"
            articles = Articles.objects.filter(article_name__startswith=article_input)
        elif datatype_input == datatype_dict[3]:
            datatype = "Categoría"
            category_object = Categories.objects.filter(category_name__startswith=article_input)
            articles = Articles.objects.filter(category_id__in=category_object)
        elif datatype_input == datatype_dict[4]:
            datatype = "Color"
            color_object = Colors.objects.filter(color_name__startswiths=article_input)
            articles = Articles.objects.filter(color_id__in=color_object)
        elif datatype_input == datatype_dict[5]:
            datatype = "Material"
            material_object = Materials.objects.filter(material_name__startswith=article_input)
            articles = Articles.objects.filter(material_id__in=material_object)
        elif datatype_input == datatype_dict[6]:
            datatype = "Talle/Tamaño"
            size_object = Sizes.objects.filter(size_name__startswith=article_input)
            articles = Articles.objects.filter(size_id__in=size_object)
        elif datatype_input == datatype_dict[7]:
            datatype = "Precio de compra"
            articles = Articles.objects.filter(buy_price__startswith=article_input)
        elif datatype_input == datatype_dict[8]:
            datatype = "Incremento"
            articles = Articles.objects.filter(increase__startswith=article_input)
        else: #datatype_input == datatype_dict[9]:
            datatype = "Precio de venta"
            articles = Articles.objects.filter(sell_price__startswith=article_input)
        
        if not articles:
            """If article is not found"""

            template = 'articles_search_not_found.html'
            context={"article_input":article_input, "articles_any": articles, "datatype_input": datatype }
            return articles_deliver(request, template, context)
        
        else:

            template="articles_search_right.html"
            context={"article_input":article_input, "articles_any": articles, "datatype_input": datatype}
            return articles_deliver(request, template, context)
    
    else:

        template="articles_search_input_empty.html"
        articles = Articles.objects.all()
        context = {"articles_any": articles}
        return articles_deliver(request, template, context)
    
### Articles create
def articles_create(request):

    categories = Categories.objects.all()
    colors = Colors.objects.all()
    materials = Materials.objects.all()
    sizes = Sizes.objects.all()
    context = {"categories":categories,
               "colors":colors,
               "materials":materials,
               "sizes":sizes}
    template='articles_create.html'

    return articles_deliver(request, template, context)

def articles_create_name_check(request):

    context = {}
    article_name_input = request.GET['article_name_input']
    template = "articles_create_name_error.html"
    context.update(name_check(article_name_input))
    return articles_deliver(request, template, context)

def articles_create_category_check(request):
    
    context = {}
    article_category_input = request.GET['article_category_input']
    context.update(category_check(article_category_input, context))
    template = "articles_create_category_error.html"
    return articles_deliver(request, template, context)
    
def articles_create_calculator(request):
    context = {}
    buy_price = request.GET['article_buy_price_input']
    increase = request.GET['article_increase_input']
    error_any = False

    if is_empty(increase) or is_empty(buy_price):

        error_any = True
        context["answer_empty_error"] = "Debes completar los campos para calcular el precio de venta"

    if not buy_price.replace(".","0",1).isnumeric() or  not increase.replace(".","0",1).isnumeric():
        error_any = True
        context["answer_string_error"] = "Los datos ingresados deben ser numéricos"
        
    if error_any:
        "show any error"
        template = "articles_create_calculator_error.html"
        return articles_deliver(request, template, context)
    
    else:

        
            
        buy_price_float = float(buy_price)
        increase_float = float(increase)
        calculator = buy_price_float + ((buy_price_float * increase_float) / 100)
        context["answer_calculator"] = calculator
        template = "articles_create_calculator_right.html"

    return articles_deliver(request, template, context)
    
def articles_create_confirm(request):
      
    any_error = False
    context = {}

    article_name_input = request.GET["article_name_input"]
    article_category_input = request.GET['article_category_input']
    article_color_input = request.GET['article_color_input']
    article_material_input = request.GET['article_material_input']
    article_size_input = request.GET['article_size_input']
    article_buy_price_input = request.GET['article_buy_price_input']
    article_increase_input = request.GET['article_increase_input']
    article_sell_price_input = request.GET['article_sell_price_input']

    context.update({
        "article_name_input": article_name_input,
        "article_category_input": str_to_int_if_possible(article_category_input),
        "article_color_input":str_to_int_if_possible(article_color_input),
        "article_material_input":str_to_int_if_possible(article_material_input),
        "article_size_input":str_to_int_if_possible(article_size_input),
        "article_buy_price_input":article_buy_price_input,
        "article_increase_input":article_increase_input,
        "article_sell_price_input":article_sell_price_input,
                })
    
    # conditions to save
    any_error, context = search_any_error(article_name_input, article_category_input, article_sell_price_input, context)
    
    categories = Categories.objects.all()
    materials = Materials.objects.all()
    colors = Colors.objects.all()
    sizes = Sizes.objects.all()

    context.update({
            "categories":categories,
            "materials":materials,
            "colors":colors,
            "sizes":sizes,
        })
    
    # end of conditions to save 
    if any_error == True:

        # for render error answers
        template = 'articles_create_save_error.html'
        context["answer_save_error"] = "No se ha creado el artículo."
        return articles_deliver(request, template, context)
    
    else:

        objects = get_objects(article_category_input,article_color_input,article_material_input,article_size_input)

        article = Articles(
            article_name = title(article_name_input),
            category_id = objects["article_category_object"],
            color_id = objects["article_color_object"],
            material_id = objects["article_material_object"],
            size_id = objects["article_size_object"], 
            buy_price = float(article_buy_price_input), 
            increase = float(article_increase_input),
            sell_price = float(article_sell_price_input.replace(',', '.'))
            )

        article.save()

        template = "articles_create_save_right.html"

        context["answer_save_right"] = f"El artículo {article.article_name} se ha guardado correctamente"
        context["answer_article_name"] = ""
        context["answer_category_id"] = ""
        context["answer_sell_price"] = ""

        return articles_deliver(request, template, context)

#Articles delete ##REVISAR EL CONTEXTO
@csrf_protect
def articles_delete(request, id):

    context = {}

    try:

        article_to_delete = get_object_or_404(Articles, id=id)

    except Exception as e:
        context["article_to_delete"] = article_to_delete
        template = "articles_delete_error.html"
        return articles_deliver(request, template, context)
    
    else:
        context["article_deleted_name"] = article_to_delete.article_name
        article_to_delete.delete() 

        template = "articles_delete_right.html"
        answer = "Artículos en la Base de datos"

        articles = Articles.objects.all()

        context.update({"articles_all":articles,
                   "articles_any": articles,
                   "answer":answer,
                   })
        
        return articles_deliver(request, template, context)

@csrf_protect
def articles_update(request, id):
    """Show update form for the article chosed """

    article_to_update = get_object_or_404(Articles, id=id)

    context={}

    categories = Categories.objects.all()
    colors = Colors.objects.all()
    materials = Materials.objects.all()
    sizes = Sizes.objects.all()
    
    
    article_category_object = article_to_update.category_id
    article_color_object = article_to_update.color_id
    article_material_object = article_to_update.material_id
    article_size_object = article_to_update.size_id

    article_category_input = article_category_object.id

    try:
        article_color_input = article_color_object.id
    except:
        article_color_input = 'Empty'

    try:
        article_material_input = article_material_object.id
    except:
        article_material_input = 'Empty'
        
    try:
        article_size_input = article_size_object.id
    except:
        article_size_input = 'Empty'

    

    context.update({"article_category_input":article_category_input,
                    "article_color_input":article_color_input,
                    "article_material_input":article_material_input,
                    "article_size_input":article_size_input})
    context.update({"categories":categories,
                    "colors":colors,
                    "materials":materials,
                    "sizes":sizes})
    context.update({"article_to_update":article_to_update})

    buy_price = str(article_to_update.buy_price).replace(",",".")
    increase = str(article_to_update.increase).replace(",",".")
    sell_price = article_to_update.sell_price

    context["article_buy_price_input"] = buy_price
    context["article_increase_input"] = increase
    context["article_sell_price_input"] = sell_price

    template='articles_update.html'

    return articles_deliver(request, template, context)
    
def articles_update_name_check(request, id):

    context = {}

    article_to_update = get_object_or_404(Articles, id=id)
    context.update({"article_to_update":article_to_update})

    article_name_input = request.GET['article_name_input']
    template = "articles_create_name_error.html"
    context.update(name_check(article_name_input))
    return articles_deliver(request, template, context)

def articles_update_category_check(request, id):
    
    
    context = {}

    article_to_update = get_object_or_404(Articles, id=id)
    context.update({"article_to_update":article_to_update})

    article_category_input = request.GET['article_category_input']
    context.update(category_check(article_category_input, context))
    template = "articles_create_category_error.html"
    return articles_deliver(request, template, context)

def articles_update_calculator(request, id):

    context = {}

    article_to_update = get_object_or_404(Articles, id=id)
    context.update({"article_to_update":article_to_update})

    buy_price = request.GET['article_buy_price_input']
    increase = request.GET['article_increase_input']
    error_any = False

    if is_empty(increase) or is_empty(buy_price):

        error_any = True
        context["answer_empty_error"] = "Debes completar los campos para calcular el precio de venta"

    if not buy_price.replace(".","0",1).isnumeric() or  not increase.replace(".","0",1).isnumeric():
        error_any = True
        context["answer_string_error"] = "Los datos ingresados deben ser numéricos"
        
    if error_any:
        "show any error"
        template = "articles_create_calculator_error.html"
        return articles_deliver(request, template, context)
    
    else:

        
            
        buy_price_float = float(buy_price)
        increase_float = float(increase)
        calculator = buy_price_float + ((buy_price_float * increase_float) / 100)
        context["answer_calculator"] = calculator
        template = "articles_create_calculator_right.html"

    return articles_deliver(request, template, context)

def articles_update_confirm(request, id):
      
    any_error = False
    context = {}

    article_to_update = get_object_or_404(Articles, id=id)
    
    article_name_input = request.GET["article_name_input"]
    article_category_input = request.GET['article_category_input']
    article_color_input = request.GET['article_color_input']
    article_material_input = request.GET['article_material_input']
    article_size_input = request.GET['article_size_input']
    article_buy_price_input = request.GET['article_buy_price_input']
    article_increase_input = request.GET['article_increase_input']
    article_sell_price_input = request.GET['article_sell_price_input']
    
    context.update({
    "article_name_input": article_name_input,
    "article_category_input": str_to_int_if_possible(article_category_input),
    "article_color_input":str_to_int_if_possible(article_color_input),
    "article_material_input":str_to_int_if_possible(article_material_input),
    "article_size_input":str_to_int_if_possible(article_size_input),
    "article_buy_price_input":article_buy_price_input,
    "article_increase_input":article_increase_input,
    "article_sell_price_input":article_sell_price_input,
            })

    # conditions to save
    any_error, context = search_any_error(article_name_input, article_category_input, article_sell_price_input, context)
    # end of conditions to save 

    categories = Categories.objects.all()
    colors = Colors.objects.all()
    materials = Materials.objects.all()
    sizes = Sizes.objects.all()

    context.update({
        "categories":categories,
        "colors":colors,
        "materials":materials,
        "sizes":sizes
        })
    
    if any_error == True:

        # for render error answers
        template = 'articles_update_save_error.html'
        context["answer_save_error"] = "No se ha actualizado el artículo."
        return articles_deliver(request, template, context)
    
    else:
        objects = get_objects(article_category_input,article_color_input,article_material_input,article_size_input)

        article_to_update.article_name = title(article_name_input)
        article_to_update.category_id = objects["article_category_object"]
        article_to_update.color_id = objects["article_color_object"]
        article_to_update.material_id = objects["article_material_object"]
        article_to_update.size_id = objects["article_size_object"]
        article_to_update.buy_price = float(article_buy_price_input)
        article_to_update.increase = float(article_increase_input)
        article_to_update.sell_price = float(article_sell_price_input.replace(',','.'))

        article_to_update.save()
        
        context["article_to_update"] = get_object_or_404(Articles, id=id)

        template = "articles_update_save_right.html"
        
        context["answer_article_name"] = ""
        context["answer_category_id"] = ""
        context["answer_sell_price"] = ""
        return articles_deliver(request, template, context)
## Articles Categories SECTION
def articles_categories(request):
    template = "categories.html"
    categories = Categories.objects.all()
    context = {"categories": categories}
    return articles_deliver(request, template, context)

## Articles Categories Create
def articles_categories_save(request):

    
    categories = Categories.objects.all()
    category_input = request.GET['category_input']
    context = {"category_input": category_input, "categories": categories}
    
    if category_input == "":

        template = "categories_table_empty_error.html"
        return articles_deliver(request, template, context)
    
    else:

        try:

            object = Categories(category_name = category_input)
            object.save()
            template = "categories_table_right.html"
            return articles_deliver(request, template, context)
        except Exception as e:
            print("-"*100)
            print(f"ESTE ES EL ERROR -----------> {e.__str__} ")
            print("-"*100)
            template = "categories_table_duplicate_error.html"
            return articles_deliver(request, template, context)


## Articles colors SECTION
def articles_colors(request):
    template = "colors.html"
    colors = Colors.objects.all()
    context = {"colors": colors}
    return articles_deliver(request, template, context)

## Articles colors create
def articles_colors_save(request):

    
    colors = Colors.objects.all()
    color_input = request.GET['color_input']
    context = {"color_input": color_input, "colors": colors}
    
    if color_input == "":

        template = "colors_table_empty_error.html"
        return articles_deliver(request, template, context)
    
    else:

        try:

            object = Colors(color_name = color_input)
            object.save()
            template = "colors_table_right.html"
            return articles_deliver(request, template, context)
        except Exception as e:
            print("-"*100)
            print(f"ESTE ES EL ERROR -----------> {e.__str__} ")
            print("-"*100)
            template = "colors_table_duplicate_error.html"
            return articles_deliver(request, template, context)
        
## Articles materials SECTION
def articles_materials(request):
    template = "materials.html"
    materials = Materials.objects.all()
    context = {"materials": materials}
    return articles_deliver(request, template, context)

## Articles materials create
def articles_materials_save(request):

    
    materials = Materials.objects.all()
    material_input = request.GET['material_input']
    context = {"material_input": material_input, "materials": materials}
    
    if material_input == "":

        template = "materials_table_empty_error.html"
        return articles_deliver(request, template, context)
    
    else:

        try:

            object = Materials(material_name = material_input)
            object.save()
            template = "materials_table_right.html"
            return articles_deliver(request, template, context)
        except Exception as e:
            print("-"*100)
            print(f"ESTE ES EL ERROR -----------> {e.__str__} ")
            print("-"*100)
            template = "materials_table_duplicate_error.html"
            return articles_deliver(request, template, context)

## Articles sizes SECTION

def articles_sizes(request):
    template = "sizes.html"
    sizes = Sizes.objects.all()
    context = {"sizes": sizes}
    return articles_deliver(request, template, context)

## Articles sizes create
def articles_sizes_save(request):

    
    sizes = Sizes.objects.all()
    size_input = request.GET['size_input']
    context = {"size_input": size_input, "sizes": sizes}
    
    if size_input == "":

        template = "sizes_table_empty_error.html"
        return articles_deliver(request, template, context)
    
    else:

        try:

            object = Sizes(size_name = size_input)
            object.save()
            template = "sizes_table_right.html"
            return articles_deliver(request, template, context)
        except Exception as e:
            print("-"*100)
            print(f"ESTE ES EL ERROR -----------> {e.__str__} ")
            print("-"*100)
            template = "sizes_table_duplicate_error.html"
            return articles_deliver(request, template, context)

# CUSTOMERS SECTION

def customers(request):
    return render(request, template_name="customers.html",context={})