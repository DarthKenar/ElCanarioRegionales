from django.shortcuts import render, get_object_or_404
from articles.models import Articles, Categories, Colors, Sizes, Materials
from django.http import HttpResponse
# Create your views here.

##ORDERS SECTION
def orders(request):
    return render(request, template_name="orders.html",context={})

##CUSTOMERS SECTION
def customers(request):
    return render(request, template_name="customers.html",context={})


##ARTICLES SECTION
def articles_deliver(request, context: dict): 
    
    return render(request,"articles.html", context)

def articles(request):

    answer = "Artículos en la Base de datos"
    articles = Articles.objects.all()
    context = {"articles_all":articles, "articles_any": articles, "answer":answer}
    return articles_deliver(request, context)
    
def articles_materials(request):

    answer = "Artículos en la Base de datos"
    articles = Articles.objects.all()
    context = {"articles_all":articles, "articles_any": articles, "answer":answer}
    return articles_deliver(request, context)

def articles_colors(request):

    answer = "Artículos en la Base de datos"
    articles = Articles.objects.all()
    context = {"articles_all":articles, "articles_any": articles, "answer":answer}
    return articles_deliver(request, context)

def articles_sizes(request):

    answer = "Artículos en la Base de datos"
    articles = Articles.objects.all()
    context = {"articles_all":articles, "articles_any": articles, "answer":answer}
    return articles_deliver(request, context)
    
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

            answer_negative = "No se encuentra:"

            context={"articles_searched":articles,"article_input":article_input, "articles_any": articles, "answer_negative": answer_negative, "datatype_input": datatype }
            return articles_deliver(request,context)
        
        else:

            answer = "Se está buscando:"
    
            context={"articles_searched":articles,"article_input":article_input, "articles_any": articles, "datatype_input": datatype, "answer": answer}
            return articles_deliver(request,context)
    
    else:

        answer_negative = "Por favor, completa el campo de búsqueda"
        answer = "Artículos en la Base de datos"
        articles = Articles.objects.all()
        context = {"articles_all":articles, "articles_any": articles, "answer_negative":answer_negative, "answer":answer}
        return articles_deliver(request, context)



def articles_create(request):

    categories = Categories.objects.all()
    colors = Colors.objects.all()
    materials = Materials.objects.all()
    sizes = Sizes.objects.all()

    context = {"categories":categories,"colors":colors,"materials":materials,"sizes":sizes}
    return render(request,template_name='articles_create.html',context = context)


def get_category(input: str) -> object:
    print("-----------------------")
    category_object = get_object_or_404(Categories, id = input)
    return category_object

def get_color(input: str) -> object:
    print("-----------------------")
    color_object = get_object_or_404(Colors, id = input)
    return color_object

def get_material(input: str) -> object:
    print("-----------------------")
    material_object = get_object_or_404(Materials, id = input)
    return material_object

def get_size(input: str) -> object:
    print("-----------------------")
    size_object = get_object_or_404(Sizes, id = input)
    return size_object

def articles_create_confirm(request):

    article_name_input = request.GET.get("article_name_input",None)
    article_category_input = request.GET['article_category_input']
    article_color_input = request.GET['article_color_input']
    article_material_input = request.GET['article_material_input']
    article_size_input = request.GET['article_size_input']
    article_buy_price_input = request.GET['article_buy_price_input']
    article_increase_input = request.GET['article_increase_input']
    article_sell_price_input = request.GET['article_sell_price_input']


    template = "articles_create_save_right.html"

    print("TIPO DE DATO DE article_buy_price_input -->",type(article_buy_price_input))
    print("TIPO DE DATO DE article_increase_input -->",type(article_increase_input))
    print("TIPO DE DATO DE article_sell_price_input -->",type(article_sell_price_input))

    article = Articles(
        article_name = article_name_input,
        category_id = get_category(article_category_input),
        color_id = get_color(article_color_input),
        material_id = get_material(article_material_input), 
        size_id = get_size(article_size_input), 
        buy_price = float(article_buy_price_input), 
        increase = float(article_increase_input),
        sell_price = float(article_sell_price_input.replace(',', '.'))
        )
    
    article.save()

    context = {"article_name_input": article_name_input,
               "article_category_input":article_category_input,
               "article_color_input":article_color_input,
               "article_material_input":article_material_input,
               "article_size_input":article_size_input,
               "article_buy_price_input":article_buy_price_input,
               "article_increase_input":article_increase_input,
               "article_sell_price_input":article_sell_price_input,
               "article_saved": article
               }

    return render(request,template,context)


def articles_delete(request, article_id):

    try:

        article_to_delete = get_object_or_404(Articles, id=article_id)

    except Exception as e:

        print(f"ESTE ES EL ERROR --------> {e}")
        template = "articles_delete_error.html"
        context = {"article": article_to_delete}
        return render(request, template, context)
    
    else:

        article_to_delete.delete()
        template = "articles_delete_right.html"
        context = {"article": article_to_delete}
        return render(request, template, context)
    
def articles_update(request):
    pass
    #section_articles_crud_deliver(request)


## ARTICLES_CATEGORIES

def articles_categories_deliver(request, template, context: dict): 

    return render(request,template, context)


def articles_categories(request):
    template = "categories.html"
    categories = Categories.objects.all()
    context = {"categories": categories}
    return articles_categories_deliver(request, template, context)

def articles_categories_save(request):

    
    categories = Categories.objects.all()
    category_input = request.GET['category_input']
    context = {"category_input": category_input, "categories": categories}
    
    if category_input == "":

        template = "categories_table_empty_error.html"
        return articles_categories_deliver(request, template, context)
    
    else:

        try:

            object = Categories(category_name = category_input)
            object.save()
            template = "categories_table_right.html"
            return articles_categories_deliver(request, template, context)
        except Exception as e:
            print("-"*100)
            print(f"ESTE ES EL ERROR -----------> {e.__str__} ")
            print("-"*100)
            template = "categories_table_duplicate_error.html"
            return articles_categories_deliver(request, template, context)


## ARTICLES_COLORS
## ARTICLES_MATERIALS
## ARTICLES_SIZES

#HTMX
##ARTICLES_CREATE.HTML
def sell_price_calculator(request):

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

        
