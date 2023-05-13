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

    answer = "Artículos en la Base de datos"
    context = {
                "articles_any": articles,
                "answer":answer,
                "datatype_input": 'name',
                "datatype": 'Nombre'
               }
    
    return render_login_required(request, template, context)

### Articles read
def articles_read_datatype(request):

    template = "articles_search_datatype.html"
    context = {}
    datatype_input = request.GET['datatype_input']

    
    if datatype_input.strip().isnumeric():

        datatype_input = int(datatype_input.strip())
        category = Category.objects.get(id = datatype_input)

        context.update({
            "datatype_input": category.id,
            "datatype": category.name,
            "articles_any": Article.objects.filter(characteristics_id__category_id=category),
            "values": Value.objects.filter(category_id=category)
        })

    else:

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

            context["datatype"] = "Nombre"
            
        elif datatype_input == datatype_dict[3]:

            context["datatype"] = "Precio de compra"

        elif datatype_input == datatype_dict[4]:

            context["datatype"] = "Incremento"

        else: #datatype_input == datatype_dict[5]

            context["datatype_input"] = datatype_input
            context["datatype"] = "Precio de venta"
            
        print("articles_any:", context.get("articles_any"))
        
    return render_login_required(request,template,context)

def articles_read_data(request):

    template = "articles_search_right.html"

    search_input = request.GET["search_input"]
    datatype_input = request.GET["datatype_input"]
    context = {}
    
    if string_is_empty(search_input):
        
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

    template='articles_create.html'

    categories = Category.objects.all()
    values = Value.objects.all()
    context = {"categories":categories,
               "values":values,
               }
    

    return render_login_required(request, template, context)

def articles_create_name_check(request):

    template = "articles_create_name_error.html"

    context = {}
    article_name_input = request.GET['article_name_input'].strip().title()
    context.update(name_check(article_name_input))
    context, any_error = name_already_in_db(article_name_input, Article, context)
    return render_login_required(request, template, context)

def articles_update_name_check(request, id):

    template = "articles_create_name_error.html"
    
    context = {}
    article_name_input = request.GET['article_name_input'].strip().title()
    article_to_update = Article.objects.get(id=id)
    
    if not article_name_input == article_to_update.name:
        context.update(name_check(article_name_input))
        context, any_error = name_already_in_db(article_name_input, Article, context)
    context["article_to_update"] = article_to_update
    return render_login_required(request, template, context)

def articles_create_calculator(request):
    context = {}
    buy_price = request.GET['article_buy_price_input'].replace(',', '.')
    increase = request.GET['article_increase_input'].replace(',', '.')
    error_any = False

    context, error_any = calculator_check(increase, buy_price, context)

    if error_any:
        template = "articles_create_calculator_error.html"
        """show any error"""
        return render_login_required(request, template, context)
    
    else:
        template = "articles_create_calculator_right.html"
        buy_price_float = float(buy_price)
        increase_float = float(increase)
        calculator = buy_price_float + ((buy_price_float * increase_float) / 100)
        context["answer_calculator"] = calculator
        
    return render_login_required(request, template, context)
    
def articles_create_confirm(request):
      
    any_error = False
    context = {}

    categories = Category.objects.all()
    values = Value.objects.all()

    context["categories"] = categories
    context["values"] = values

    article_name_input = request.GET["article_name_input"].strip().title()
    article_buy_price_input = request.GET['article_buy_price_input'].replace(',', '.')
    article_increase_input = request.GET['article_increase_input'].replace(',', '.')
    answer_calculator = request.GET['article_sell_price_input'].replace(',', '.')

    context.update({
        "article_name_input": article_name_input,
        "article_buy_price_input":article_buy_price_input,
        "article_increase_input":article_increase_input,
        "answer_calculator":answer_calculator,
                })
    
    # conditions to save
    error_context = {}
    error_context, search_any_error_in_name_field_bool = search_any_error_in_name_field(article_name_input, context)
    error_context, calculator_check_bool = calculator_check(article_increase_input,article_buy_price_input, context)
    error_context, name_already_in_db_bool = name_already_in_db(article_name_input, Article, context)
    values_dict = get_values_for_categories(request)
    # end of conditions to save 

    if search_any_error_in_name_field_bool == True or calculator_check_bool == True or name_already_in_db_bool == True:

        any_error = True
        context.update(error_context)

    if any_error == True:

        # for render error answers
        context.update(values_dict)
        template = 'articles_create_save_error.html'
        context["answer_save_error"] = "No se ha creado el artículo, revise los campos nuevamente."
        return render_login_required(request, template, context)

    else:

        template = "articles_create_save_right.html"

        context.pop("article_name_input")
        context.pop("article_buy_price_input")
        context.pop("article_increase_input")
        context.pop("answer_calculator")

        article = Article(
            name = title(article_name_input),
            buy_price = float(article_buy_price_input), 
            increase = float(article_increase_input),
            sell_price = float(answer_calculator)
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

        context["answer_save_right"] = f"El artículo {article.name} se ha guardado correctamente"
        context["answer_articles_name"] = ""
        context["answer_category_id"] = ""

        return render_login_required(request, template, context)

def articles_update_confirm(request, id):

    any_error = False
    context = {}

    categories = Category.objects.all()
    values = Value.objects.all()
    article_to_update = Article.objects.get(id=id)

    context["categories"] = categories
    context["values"] = values

    article_name_input = request.GET["article_name_input"].strip().title()
    article_buy_price_input = request.GET['article_buy_price_input'].replace(',', '.')
    article_increase_input = request.GET['article_increase_input'].replace(',', '.')
    answer_calculator = request.GET['article_sell_price_input'].replace(',', '.')

    context.update({
        "article_name_input": article_name_input,
        "article_buy_price_input":article_buy_price_input,
        "article_increase_input":article_increase_input,
        "answer_calculator":answer_calculator,
                })
    
    # conditions to save
    error_context = {}
    
    
    if not article_name_input == article_to_update.name:

        error_context, search_any_error_in_name_field_bool = search_any_error_in_name_field(article_name_input, context)
        error_context, name_already_in_db_bool = name_already_in_db(article_name_input, Article, context)

    error_context, calculator_check_bool = calculator_check(article_increase_input,article_buy_price_input, context)
    
    values_dict = get_values_for_categories(request)
    # end of conditions to save 
    if not article_name_input == article_to_update.name:
        if search_any_error_in_name_field_bool == True or calculator_check_bool == True or name_already_in_db_bool == True:

            any_error = True
            context.update(error_context)

    if any_error == True:

        template = 'articles_create_save_error.html'
        
        # for render error answer
        context.update(values_dict)
        context["answer_save_error"] = "No se ha creado el artículo, revise los campos nuevamente."
        context["article_to_update"] = article_to_update
        return render_login_required(request, template, context)

    else:

        template = "articles_create_save_right.html"
        
        context.pop("article_name_input")
        context.pop("article_buy_price_input")
        context.pop("article_increase_input")
        context.pop("answer_calculator")

        article_to_update.name = article_name_input
        article_to_update.buy_price = article_buy_price_input
        article_to_update.increase = article_increase_input
        article_to_update.sell_price = answer_calculator

        article_to_update.save()
        delete_old_values(article_to_update)

        for value in values_dict.values():
            if value != None:
                article_value = ArticleValue(
                    article_id = article_to_update,
                    category_id = value.category_id,
                    value_id = value
                )
                article_value.save()

        context["answer_save_right"] = f"El artículo {article_to_update.name} se ha actualizado correctamente"
        context["answer_articles_name"] = ""
        context["answer_category_id"] = ""

        return render_login_required(request, template, context)
#Articles delete
@csrf_protect
def article_delete(request, id):

    context = {}

    try:
        article_to_delete = get_object_or_404(Article, id=id)
    except Exception as e:
        template = "articles_delete_error.html"
        return render_login_required(request, template, context)
    else:
        template = "articles_delete_right.html"
        context["answer"] = f"Se eliminó correctamente el artículo {article_to_delete.name}"
        article_to_delete.delete()
        articles = Article.objects.all()
        categories = Category.objects.all()
        context.update({
                   "articles_any": articles,
                   "categories": categories
                   })
        return render_login_required(request, template, context)

@csrf_protect
def article_update(request, id):

    template = 'articles_update.html'

    context = {}
    categories = Category.objects.all()
    values = Value.objects.all()
    context = {"categories":categories,
               "values":values,
               }
    article_to_update = Article.objects.get(id = id)
    context['article_to_update'] = article_to_update
    return render_login_required(request, template, context)    

# ## Articles Categorie SECTION
def articles_categories(request):

    template = "categories.html"

    categories = Category.objects.all()
    context = {}
    context["categories"] = categories
    return render_login_required(request, template, context)

def articles_category_create(request, art_id=None):

    category_name = request.POST["category_name_new"].strip().title()
    context = {}
    context["categories"] = Category.objects.all()

    template = "articles_category_section.html"
    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['articles_any'] = [article_to_update]

    any_error = False
    error_context, search_any_error_in_name_field_bool = search_any_error_in_name_field(category_name, context)
    error_context, name_already_in_db_bool = name_already_in_db(category_name, Category, context)
    error_context, is_empty_name_bool = is_empty_name(category_name, context)
    error_context, name_already_in_db_bool = name_already_in_db(category_name, Category, context)

    if search_any_error_in_name_field_bool == True or name_already_in_db_bool == True or is_empty_name_bool == True:
        any_error = True
        context = error_context

    if any_error == False:
        category_to_save = Category(name=category_name)
        category_to_save.save()
        context['category_to_update'] = category_to_save
        context["answer_title_values"] = f"Agregar valores a: {category_to_save.name}"
        context["answer"] = f"La categoría {category_to_save.name} se ha guardado correctamente!"
    else:
        context["answer"] = "No se ha podido guardar la categoría!"

    return render_login_required(request, template, context)

def articles_category_value_create(request,cat_id, art_id=None):

    context={}
    context["categories"] = Category.objects.all()

    category_to_update = Category.objects.get(id = cat_id)
    context['category_to_update'] = category_to_update

    value_name = request.POST['value_name_new'].strip().title()
    any_error = False
    context, name_already_in_db_bool = name_already_in_db(value_name, Value, context)
    context, is_empty_name_bool = is_empty_name(value_name, context)

    template = 'articles_category_section.html'
    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['articles_any'] = [article_to_update]

    if name_already_in_db_bool == True or is_empty_name_bool == True:
        any_error = True
    
    if any_error == False:
        val = Value(
            category_id = category_to_update,
            name = value_name
                    )
        val.save()
        context['answer'] = f'Se guardó correctamente el valor: {value_name} , para la categoría: {category_to_update.name}'
        context['values'] = Value.objects.filter(category_id = category_to_update)
    else:
        context["answer"] = f"No se ha podido guardar el valor: {value_name}, para la categoría: {category_to_update.name}"
        context['values'] = Value.objects.filter(category_id = category_to_update)

    return render_login_required(request, template, context)

def articles_category_update(request, path, cat_id, art_id=None):
    
    if "articles/categories" in path:
        template = "articles_category_section.html"
    else: 
        template = "categories.html"

    context={}
    category_to_update = Category.objects.get(id = cat_id)
    context['category_to_update'] = category_to_update

    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['articles_any'] = [article_to_update]

    context["categories"] = Category.objects.all()
    context['values'] = Value.objects.filter(category_id = category_to_update)
    context["answer_title_values"] = f"Categoría seleccionada: {category_to_update.name}"
    context["name_category_edition"] = True
    
    
    return render_login_required(request, template, context)

def articles_category_update_name(request, cat_id, art_id=None):

    context={}
    new_name = request.POST['category_name_update'].strip().title()
    context, any_error = search_any_error_in_name_field(new_name, context)
    context, any_error = name_already_in_db(new_name, Category, context)
    category_to_update = Category.objects.get(id = cat_id)
    context['category_to_update'] = category_to_update
    template = "articles_category_section.html"

    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['articles_any'] = [article_to_update]

    if any_error == False:
        
        context['answer'] = f'Se ha actualizado correctamente la categoría {category_to_update.name} --> {new_name}!'
        category_to_update.name = new_name
        category_to_update.save()
    else:
        context['answer'] = f'No se puede actualizar el nombre de la categoría {category_to_update.name} --> {new_name}!'

    context["categories"] = Category.objects.all()
    context['values'] = Value.objects.filter(category_id = category_to_update)
    context["answer_title_values"] = f"Categoría seleccionada: {category_to_update.name}"
    context["name_category_edition"] = False

    return render_login_required(request, template, context)
def articles_category_delete(request, cat_id, art_id=None):

    template = "articles_category_section.html"

    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['articles_any'] = [article_to_update]

    context={}
    category_to_update = Category.objects.get(id = cat_id)
    context["answer"] = f"La categoría {category_to_update.name} ha sido eliminada."
    category_to_update.delete()
    context["categories"] = Category.objects.all()
    return render_login_required(request, template, context)

def articles_value_delete(request, cat_id, val_id, art_id=None):

    context={}
    val = Value.objects.get(id = val_id)
    art_id = request.GET.get('art_id')

    template = "articles_category_section.html"
    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['articles_any'] = [article_to_update]

    category_to_update = Category.objects.get(id = cat_id)
    context['category_to_update'] = category_to_update
    
    context["answer"] = f"De la categoría {category_to_update.name}, el valor {val.name} ha sido eliminado."
    val.delete()



    context["categories"] = Category.objects.all()
    context['values'] = Value.objects.filter(category_id = category_to_update)
    return render_login_required(request, template, context)


def articles_value_update(request, cat_id, val_id, art_id=None):

    context={}
    val = Value.objects.get(id = val_id)

    template = "articles_category_section.html"
    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['articles_any'] = [article_to_update]

    category_to_update = Category.objects.get(id = cat_id)
    context['category_to_update'] = category_to_update

    context["categories"] = Category.objects.all()
    
    context['value_to_update'] = val
    context['values'] = Value.objects.filter(category_id = category_to_update)
    context["answer_title_values"] = f"Categoría seleccionada: {category_to_update.name}"
    context["name_value_edition"] = True
    return render_login_required(request, template, context)

def articles_value_update_name(request,cat_id, val_id, art_id=None):

    context={}
    new_name = request.POST['value_name_update'].strip().title()
    context, any_error = name_already_in_db(new_name, Category, context)
    context, any_error = is_empty_name(new_name, context)
    val = Value.objects.get(id = val_id)

    category_to_update = Category.objects.get(id = cat_id)
    context['category_to_update'] = category_to_update

    template = "articles_category_section.html"
    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['articles_any'] = [article_to_update]
    
    if any_error == False:
        val.name = new_name
        val.save()
        context['answer'] = f'Se ha actualizado correctamente el valor {val.name} --> {new_name}!'
    else:
        context['answer'] = f'No se puede actualizar el nombre del valor{val.name} --> {new_name}!'

    context['value_to_update'] = val
    context["categories"] = Category.objects.all()
    context['values'] = Value.objects.filter(category_id = category_to_update)
    context["answer_title_values"] = f"Categoría seleccionada: {category_to_update.name}"
    context["name_value_edition"] = False

    return render_login_required(request, template, context)

def customers(request):

    template="customers.html"

    return render_login_required(request, template,context={})
