from django.shortcuts import render, get_object_or_404
from articles.models import Articles, Categories, Colors, Sizes, Materials
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

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

    article_name_input = request.GET['article_name_input']

    if article_name_input == '':

        template = "articles_create_name_error.html"
        context = {"answer_article_name": "Este campo es obligatorio"}
        return articles_deliver(request, template, context)

    elif not article_name_input.isalpha():

        template = "articles_create_name_error.html"
        context = {"answer_article_name": "El nombre del artículo no debe contener números, simbolos o espacios."}
        return articles_deliver(request, template, context)
    
    else:

        template = "articles_create_name_error.html"
        context = {"answer_article_name": ""}
        return articles_deliver(request, template, context)
    
def articles_create_category_check(request):
    
    article_category_input = request.GET['article_category_input']
    print(article_category_input)

    if article_category_input == 'Empty':

        context = {"answer_category_id": "Es obligatorio seleccionar una categoría."}
        template = "articles_create_category_error.html"
        return articles_deliver(request, template, context)
    
    else:
        context = {"answer_category_id": ""}
        template = "articles_create_category_error.html"
        return articles_deliver(request, template, context)
    
def articles_create_confirm_get_category(input: str) -> object:
    category_object = get_object_or_404(Categories, id = input)
    return category_object
def articles_create_confirm_get_color(input: str) -> object:
    color_object = get_object_or_404(Colors, id = input)
    return color_object
def articles_create_confirm_get_material(input: str) -> object:
    material_object = get_object_or_404(Materials, id = input)
    return material_object
def articles_create_confirm_get_size(input: str) -> object:
    size_object = get_object_or_404(Sizes, id = input)
    return size_object

def articles_create_sell_price_calculator(request):

    buy_price = request.GET['article_buy_price_input']
    increase = request.GET['article_increase_input']

    if (buy_price != "" and buy_price.isalpha()) or  (increase != "" and increase.isalpha()):

        return render(request, template_name='articles_create_calculator_string_error.html')

    elif increase == "" or buy_price == "":

        return render(request, template_name='articles_create_calculator_empty.html')
    
    else:

        try:

            buy_price_float = float(buy_price)
            increase_float = float(increase)

        except ValueError:

            return render(request, template_name='articles_create_calculator_string_error.html')
        
        else:

            calculator =buy_price_float + ((buy_price_float * increase_float) / 100)
            context = {"answer_calculator": calculator}
            return render(request, template_name='articles_create_calculator_right.html', context=context)

def articles_create_confirm(request):
    
    categories = Categories.objects.all()
    colors = Colors.objects.all()
    materials = Materials.objects.all()
    sizes = Sizes.objects.all()

    
    any_error = False

    article_name_input = request.GET["article_name_input"]
    article_category_input = request.GET['article_category_input']
    article_color_input = request.GET['article_color_input']
    article_material_input = request.GET['article_material_input']
    article_size_input = request.GET['article_size_input']
    article_buy_price_input = request.GET['article_buy_price_input']
    article_increase_input = request.GET['article_increase_input']
    article_sell_price_input = request.GET['article_sell_price_input']

    if article_category_input != 'Empty':
        article_category_input= int(article_category_input)

    context = {"article_name_input": article_name_input,
                "article_category_input":article_category_input,
                "article_color_input":article_color_input,
                "article_material_input":article_material_input,
                "article_size_input":article_size_input,
                "article_buy_price_input":article_buy_price_input,
                "article_increase_input":article_increase_input,
                "article_sell_price_input":article_sell_price_input,
                }
    
    context_variables = {"categories":categories,
                         "colors":colors,
                         "materials":materials,
                         "sizes":sizes}
    context.update(context_variables)

    # conditions to save
    if article_name_input == '':
        any_error = True
        context['answer_article_name'] = 'Es obligatorio completar el nombre.'
    elif not article_name_input.isalpha():
        any_error = True
        context['answer_article_name'] = 'El nombre del artículo no debe contener números, simbolos o espacios.'

    if article_category_input == 'Empty':
        any_error = True
        context['answer_category_id'] = 'Es obligatorio seleccionar una categoría.'
    

    if article_buy_price_input == '' or article_increase_input == '' or article_sell_price_input == '':
        any_error = True
        context['answer_sell_price'] = "No puede guardar un artículo sin haber calculado el precio de venta. Intentelo nuevamente"

    # end of conditions to save 
    if any_error == True:

        # for render error answers
        template = 'articles_create_save_error.html'
        return articles_deliver(request, template, context)
    
    else:

        if article_color_input != 'Empty':
            article_color_input = articles_create_confirm_get_color(article_color_input)
        else:
            article_color_input = None

        if article_material_input != 'Empty':
            article_material_input = articles_create_confirm_get_material(article_material_input)
        else:
            article_material_input = None

        if article_size_input != 'Empty':
            article_size_input = articles_create_confirm_get_size(article_size_input)
        else:
            article_size_input = None

        article = Articles(
            article_name = article_name_input,
            category_id = articles_create_confirm_get_category(article_category_input),
            color_id = article_color_input,
            material_id = article_material_input,
            size_id = article_size_input, 
            buy_price = float(article_buy_price_input), 
            increase = float(article_increase_input),
            sell_price = float(article_sell_price_input.replace(',', '.'))
            )

        article.save()
        template = "articles_create_save_right.html"
        context["article_saved"] = article

        context["answer_article_name"] = ""
        context["answer_category_id"] = ""
        context["answer_sell_price"] = ""

        return articles_deliver(request, template, context)

#Articles delete ##REVISAR EL CONTEXTO
@csrf_protect
def articles_delete(request, id):

    try:

        article_to_delete = get_object_or_404(Articles, id=id)

    except Exception as e:

        print(f"ESTE ES EL ERROR --------> {e}")
        template = "articles_delete_error.html"
        context = {}
        return articles_deliver(request, template, context)
    
    else:
        
        article_to_delete.delete() 
        #puede que tenga un error de logica porque puede que borre el objeto antes de guardarlo en el contexto y mostrarlo en el template
        template = "articles_delete_right.html"
        answer = "Artículos en la Base de datos"
        articles = Articles.objects.all()
        context = {"articles_all":articles,
                   "articles_any": articles,
                   "answer":answer,
                   "article": article_to_delete}
        return articles_deliver(request, template, context)

#Articles update
@csrf_protect
def articles_update(request, id):
    """Show update form for the article chosed """

    try:

        article_to_update = get_object_or_404(Articles, id=id)

    except:

        template = "articles_update_form_error.html"
        context={}
        return articles_deliver(request, template, context)
    
    else:

        context={}

        categories = Categories.objects.all()
        colors = Colors.objects.all()
        materials = Materials.objects.all()
        sizes = Sizes.objects.all()
        """Obtener categorias colores talles y materiales, guardarlos en variables y pasarlos como contexto"""
        
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
        context.update({"article":article_to_update})

        template='articles_update.html'

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