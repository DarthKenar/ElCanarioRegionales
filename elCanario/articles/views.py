from django.shortcuts import render, get_object_or_404, redirect
from articles.models import Category, Value, Article, ArticleValue, Customer, Stock, Promotion, Order, Expense
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from .utils import *



# # ORDERS SECTION
def orders(request):

    template = "orders.html"

    return render_login_required(request, template,context={})

# # ARTICLEs SECTION

def articles(request):

    template = "articles.html"

    articles = Article.objects.all()
    categories = Category.objects.all()

    answer = "Artículos en la Base de datos"
    context = {
                "articles_any": articles,
                "answer":answer,
                "categories": categories,
                "datatype_input": 'name',
                "datatype": 'Nombre'
               }
    
    return render_login_required(request, template, context)

### Articles read
def articles_read_datatype(request):

    template = "articles_search_datatype.html"
    context = {}
    datatype_input = request.GET['datatype_input']

    categories = Category.objects.all()
    context["categories"] = categories
    
    if datatype_input.strip().isnumeric():

        datatype_input = int(datatype_input.strip())
        category = Category.objects.get(id = datatype_input)

        context["articles_any"] = Article.objects.filter(characteristics_id__category_id=category)
        
        context["datatype_input"] = category.id
        context["datatype"] = category.name

        context["values"] = Value.objects.filter(category_id=category)
    else:

        datatype_dict = {
                        1: "id",
                        2: "name",
                        3: "buy_price",
                        4: "increase",
                        5: "sell_price"
                        }
        
        articles = Article.objects.all()
        context["datatype_input"] = datatype_input
        context["articles_any"] = articles

        if datatype_input == datatype_dict[1]:

            context["datatype_input"] = datatype_input
            context["datatype"] = "Id"

        elif datatype_input == datatype_dict[2]:

            context["datatype"] = "Nombre"
            
        elif datatype_input == datatype_dict[3]:

            context["datatype"] = "Precio de compra"

        elif datatype_input == datatype_dict[4]:

            context["datatype"] = "Incremento"

        else: #datatype_input == datatype_dict[5]

            context["datatype_input"] = datatype_input
            context["datatype"] = "Precio de venta"
            

    return render_login_required(request,template,context)

def articles_read_data(request):

    template = "articles_search_right.html"

    search_input = request.GET["search_input"]
    datatype_input = request.GET["datatype_input"]
    context = {}
    
    if is_empty(search_input):
        
        template = "articles_search_input_empty.html"
        context["articles_any"] = Article.objects.all()

    elif datatype_input.strip().isnumeric():
        
        datatype_input = int(datatype_input)
        search_input = int(search_input)

        category = Category.objects.get(id = datatype_input)
        value = Value.objects.get(id = search_input)
        context["articles_any"] = Article.objects.filter(characteristics_id=value)
        context["datatype_input"] = category.id
        context["datatype"] = category.name
        context["value"] = value.name

    else:
        search_input = search_input.strip()
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

    if value_in_context_is_empty(context["articles_any"]):
        template = "articles_search_not_found.html"
        
    categories = Category.objects.all()
    context["search_input"] = search_input
    context["categories"] = categories

    return render_login_required(request, template, context)

### Articles create
def articles_create(request):

    categories = Category.objects.all()
    values = Value.objects.all()
    context = {"categories":categories,
               "values":values,
               }
    template='articles_create.html'

    return render_login_required(request, template, context)

def articles_create_name_check(request):

    context = {}
    article_name_input = request.GET['article_name_input']
    template = "articles_create_name_error.html"
    context.update(name_check(article_name_input))
    return render_login_required(request, template, context)

def articles_create_calculator(request):
    context = {}
    buy_price = request.GET['article_buy_price_input']
    increase = request.GET['article_increase_input']
    error_any = False

    context, error_any = calculator_check(increase, buy_price)

    if error_any:
        """show any error"""
        template = "articles_create_calculator_error.html"
        return render_login_required(request, template, context)
    
    else:

        buy_price_float = float(buy_price)
        increase_float = float(increase)
        calculator = buy_price_float + ((buy_price_float * increase_float) / 100)
        context["answer_calculator"] = calculator
        template = "articles_create_calculator_right.html"

    return render_login_required(request, template, context)
    
def articles_create_confirm(request):
      
    any_error = False
    context = {}

    categories = Category.objects.all()
    values = Value.objects.all()
    context["categories"] = categories
    context["values"] = values
    article_name_input = request.GET["article_name_input"]
    article_buy_price_input = request.GET['article_buy_price_input']
    article_increase_input = request.GET['article_increase_input']
    article_sell_price_input = request.GET['article_sell_price_input']

    context.update({
        "article_name_input": article_name_input,
        "article_buy_price_input":article_buy_price_input,
        "article_increase_input":article_increase_input,
        "article_sell_price_input":article_sell_price_input,
                })
    
    # conditions to save
    context, any_error = search_any_error(article_name_input, article_sell_price_input, context)
    values_dict = get_values_for_categories(request)
    # end of conditions to save 
    
    if any_error == True:

        # for render error answers
        context.update(values_dict)
        template = 'articles_create_save_error.html'
        context["answer_save_error"] = "No se ha creado el artículo, revise los campos nuevamente."
        return render_login_required(request, template, context)

    else:

        article = Article(
            name = title(article_name_input),
            buy_price = float(article_buy_price_input), 
            increase = float(article_increase_input),
            sell_price = float(article_sell_price_input.replace(',', '.'))
            )
        
        article.save()

        

        for value in values_dict.values():
            if value != None:

                article_value = ArticleValue(
                    article_id = article,
                    category_id = value.category_id,
                    value_id = value
                )
                article_value.save()

        template = "articles_create_save_right.html"

        context["answer_save_right"] = f"El artículo {article.name} se ha guardado correctamente"
        context["answer_articles_name"] = ""
        context["answer_category_id"] = ""
        context["answer_sell_price"] = ""

        return render_login_required(request, template, context)

#Articles delete ##REVISAR EL CONTEXTO
@csrf_protect
def article_delete(request, id):

    context = {}

    try:

        article_to_delete = get_object_or_404(Article, id=id)

    except Exception as e:
        template = "articles_delete_error.html"
        return render_login_required(request, template, context)
    
    else:
        context["answer"] = f"Se eliminó correctamente el artículo {article_to_delete.name}"
        article_to_delete.delete()
        template = "articles_delete_right.html"

        articles = Article.objects.all()

        context.update({
                   "articles_any": articles,
                   })
        
        return render_login_required(request, template, context)

@csrf_protect
def article_update(request, id):
    context = {}
    categories = Category.objects.all()
    values = Value.objects.all()
    context = {"categories":categories,
               "values":values,
               }
    template = 'articles_update.html'
    article_to_update = Article.objects.get(id = id)
    context['article_to_update'] = article_to_update
    return render_login_required(request, template, context)    

# ## Articles Categorie SECTION
def articles_categories(request):

    categories = Category.objects.all()
    template = "categories.html"
    context = {}
    context["categories"] = categories
    return render_login_required(request, template, context)

def articles_categories_create(request):

    category_name = request.POST["category_name_new"].strip().title()
    
    context = {}
    context["categories"] = Category.objects.all()
    any_error = False
    context, any_error = search_any_error_in_name_field(category_name, context)
    context, any_error = name_already_in_db(category_name, Category, context)
    context, any_error = is_empty_name(category_name, context)
    if any_error == False:
        cat = Category(name=category_name)
        cat.save()
        context['category_selected'] = cat
        context["answer_title_values"] = f"Agregar valores a: {cat.name}"
        template = "articles_category_section_right.html"
        context["answer"] = f"La categoría {cat.name} se ha guardado correctamente!"
    else:
        template = "articles_category_section_error.html"
        context["answer"] = "No se ha podido guardar la categoría!"

    return render_login_required(request, template, context)

def articles_category_value_create(request,id):
    context={}
    context["categories"] = Category.objects.all()
    cat = Category.objects.get(id = id)
    context['category_selected'] = cat
    value_name = request.POST['value_name_new'].strip().title()
    
    context, any_error = string_has_internal_spaces(value_name, context)
    context, any_error = name_already_in_db(value_name, Category, context)
    context, any_error = is_empty_name(value_name, context)
    if any_error == False:
        val = Value(
            category_id = cat,
            name = value_name
                    )
        val.save()
        template = 'articles_category_section_right.html'
        context['answer'] = f'Se guardó correctamente el valor: {value_name} , para la categoría: {cat.name}'
        context['values'] = Value.objects.filter(category_id = cat)
    else:
        
        context["answer"] = f"No se ha podido guardar el valor: {value_name}, para la categoría: {cat.name}"
        template = 'articles_category_section_error.html'
        context['values'] = Value.objects.filter(category_id = cat)

    return render_login_required(request, template, context)

def articles_category_update(request,id, path):

    if "articles_categories" in path:
        template = "articles_category_section_right.html"
    else: 
        template = "categories.html"
    context={}
    cat = Category.objects.get(id = id)
    context["categories"] = Category.objects.all()
    context['category_selected'] = cat
    context['values'] = Value.objects.filter(category_id = cat)
    context["answer_title_values"] = f"Categoría seleccionada: {cat.name}"
    context["name_category_edition"] = True
    
    return render_login_required(request, template, context)

def articles_category_update_name(request, id):
    context={}
    new_name = request.POST['category_name_update'].strip().title()
    context, any_error = search_any_error_in_name_field(new_name, context)
    context, any_error = name_already_in_db(new_name, Category, context)
    cat = Category.objects.get(id = id)
    if any_error == False:
        context['answer'] = f'Se ha actualizado correctamente la categoría {cat.name} --> {new_name}!'
        cat.name = new_name
        cat.save()
        template = "articles_category_section_right.html"
    else:
        context['answer'] = f'No se puede actualizar el nombre de la categoría {cat.name} --> {new_name}!'
        template = "articles_category_section_error.html"
    context['category_selected'] = cat
    context["categories"] = Category.objects.all()
    context['values'] = Value.objects.filter(category_id = cat)
    context["answer_title_values"] = f"Categoría seleccionada: {cat.name}"
    context["name_category_edition"] = False

    return render_login_required(request, template, context)
def articles_category_delete(request, id):

    context={}
    cat = Category.objects.get(id = id)
    context["answer"] = f"La categoría {cat.name} ha sido eliminada."
    cat.delete()
    context["categories"] = Category.objects.all()
    template = "articles_category_section_right.html"
    return render_login_required(request, template, context)

def articles_value_delete(request, id):

    context={}
    val = Value.objects.get(id = id)
    cat = val.category_id
    context["answer"] = f"De la categoría {cat.name}, el valor {val.name} ha sido eliminado."
    val.delete()
    context["categories"] = Category.objects.all()
    template = "articles_category_section_right.html"
    context['values'] = Value.objects.filter(category_id = cat)
    context['category_selected'] = cat
    return render_login_required(request, template, context)


def articles_value_update(request, id):

    context={}
    val = Value.objects.get(id = id)
    cat = val.category_id
    context["categories"] = Category.objects.all()
    context['category_selected'] = cat
    context['value_selected'] = val
    context['values'] = Value.objects.filter(category_id = cat)
    context["answer_title_values"] = f"Categoría seleccionada: {cat.name}"
    context["name_value_edition"] = True
    template = "articles_category_section_right.html"
    return render_login_required(request, template, context)

def articles_value_update_name(request, id):
    context={}
    new_name = request.POST['value_name_update'].strip().title()
    context, any_error = name_already_in_db(new_name, Category, context)
    context, any_error = is_empty_name(new_name, context)
    val = Value.objects.get(id = id)
    cat = val.category_id
    context['category_selected'] = cat
    if any_error == False:
        val.name = new_name
        val.save()
        template = "articles_category_section_right.html"
        context['answer'] = f'Se ha actualizado correctamente el valor {val.name} --> {new_name}!'
    else:
        context['answer'] = f'No se puede actualizar el nombre del valor{val.name} --> {new_name}!'
        template = "articles_category_section_error.html"
    context['value_selected'] = val
    context["categories"] = Category.objects.all()
    context['values'] = Value.objects.filter(category_id = cat)
    context["answer_title_values"] = f"Categoría seleccionada: {cat.name}"
    context["name_value_edition"] = False

    return render_login_required(request, template, context)

def customers(request):
    template="customers.html"
    return render_login_required(request, template,context={})