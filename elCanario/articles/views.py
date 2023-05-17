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

    datatype_input = request.GET['datatype_input'].strip()
    
    if datatype_input.isnumeric():
        """if numeric, the user has selected some category as data type"""

        context.update(get_articles_by_category_datatype(datatype_input))

    else:
        """if not numeric, the user has selected some article native field as data type"""
        
        context.update(get_articles_by_native_datatype(datatype_input))

    return render_login_required(request,template,context)

def articles_read_data(request):

    template = "articles_search_data.html"

    search_input = request.GET["search_input"].strip()
    datatype_input = request.GET["datatype_input"].strip()
    context = {}
    
    if datatype_input.isnumeric():
        """comprueba que la seleccion del usuario sea una categoría"""

        if string_is_empty(search_input):
            """trae todos los artículos que contengan valores en esa categoría"""
            context.update(get_articles_by_category_datatype(datatype_input))

        else:
            """trae todos los artículos que tengan ese valor específico"""
            context.update(get_articles_for_value_of_category(datatype_input,search_input))

    else:
        """el usuario ha seleccionado como tipo de búsqueda un tipo de dato nativo, (no categoría)"""

        if string_is_empty(search_input):
            """Si el campo de búsqueda está vacío se mostrarán todos los artículos"""
            context["articles_any"] = Article.objects.all()

        else:
            """Si el campo de búsqueda no está vacío, se buscará de acuerdo a un tipo de dato nativo, (no categoría)"""
            context.update(get_articles_for_search_input_in_native_datatype(datatype_input, search_input))


    # if value_in_context_is_empty(context["articles_any"]):
    #     """Una vez que realiza la búsqueda de artículos, si no se encuentran, trae todos igualmente en vez de no traer ninguno"""
    #     template = "articles_search_data.html"
        
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

    template = "articles_create_calculator.html"


    context = {}
    buy_price = request.GET['article_buy_price_input'].replace(',', '.')
    increase = request.GET['article_increase_input'].replace(',', '.')
    error_any = False

    context, error_any = calculator_check(increase, buy_price, context)

    if error_any:
        """show any error"""
        return render_login_required(request, template, context)
    
    else:
        
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
    template = "articles_search_data.html"
    try:
        article_to_delete = get_object_or_404(Article, id=id)
    except Exception as e:
        
        return render_login_required(request, template, context)
    else:
        
        context["article_delete_answer"] = f"Se eliminó correctamente el artículo {article_to_delete.name}"
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

    template = 'articles_category_value_section.html'
    category_name = request.POST["category_name_new"].strip().title()
    context = {}
    context["categories"] = Category.objects.all()

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

    template = 'articles_category_value_section.html'

    context={}
    context["categories"] = Category.objects.all()

    category_to_update = Category.objects.get(id = cat_id)
    context['category_to_update'] = category_to_update

    value_name = request.POST['value_name_new'].strip().title()
    any_error = False
    context, name_already_in_db_bool = name_already_in_db(value_name, Value, context)
    context, is_empty_name_bool = is_empty_name(value_name, context)

    
    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['articles_any'] = [article_to_update]

    if name_already_in_db_bool == True or is_empty_name_bool == True:
        any_error = True
    
    if any_error == False:
        value_to_update = Value(
            category_id = category_to_update,
            name = value_name
                    )
        value_to_update.save()
        context['answer'] = f'Se guardó correctamente el valor: {value_name} , para la categoría: {category_to_update.name}'
        context['values'] = Value.objects.filter(category_id = category_to_update)
    else:
        context["answer"] = f"No se ha podido guardar el valor: {value_name}, para la categoría: {category_to_update.name}"
        context['values'] = Value.objects.filter(category_id = category_to_update)

    return render_login_required(request, template, context)

def articles_category_update(request, external_link, cat_id, art_id=None):
    print("external_link -->", external_link)
    
    print("External Link type", type(external_link))
    print("CAT_ID -->", cat_id)
    print("ART_ID -->", art_id)
    external_link = str_to_bool_external_link(external_link)

    if external_link == False:
        print("NOT EXTERNAL LINK", external_link)
        print("External Link type", type(external_link))
        template = "articles_category_value_section.html"
    else: 
        print("EXTERNAL LINK", external_link)
        print("External Link type", type(external_link))
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

    template = 'articles_category_value_section.html'
    context={}

    category_to_update = Category.objects.get(id = cat_id)
    context['category_to_update'] = category_to_update

    new_name = request.POST['category_name_update'].strip().title()
    context, search_any_error_in_name_field_bool = search_any_error_in_name_field(new_name, context)
    context, name_already_in_db_bool = name_already_in_db(new_name, Category, context)
    context, is_the_same_name_bool = is_the_same_name(new_name, category_to_update.name, context)

    #REVISAR SI SE PUEDE CREAR UNA FUNCION EN UTILS QUE HAGA ESTO YA QUE SE REPITE ESTA PORCION EN VARIOS LADOS 'if not string_is_empty'
    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['articles_any'] = [article_to_update]

    if search_any_error_in_name_field_bool == False and is_the_same_name_bool == False and name_already_in_db_bool == False:
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

    template = 'articles_category_value_section.html'

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

    template = 'articles_category_value_section.html'

    context={}
    value_to_update = Value.objects.get(id = val_id)

    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['articles_any'] = [article_to_update]

    category_to_update = Category.objects.get(id = cat_id)
    context['category_to_update'] = category_to_update
    
    context["answer"] = f"De la categoría {category_to_update.name}, el valor {value_to_update.name} ha sido eliminado."
    value_to_update.delete()



    context["categories"] = Category.objects.all()
    context['values'] = Value.objects.filter(category_id = category_to_update)
    return render_login_required(request, template, context)


def articles_value_update(request, cat_id, val_id, art_id=None):

    context={}
    value_to_update = Value.objects.get(id = val_id)

    template = 'articles_category_value_section.html'

    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['articles_any'] = [article_to_update]

    category_to_update = Category.objects.get(id = cat_id)
    context['category_to_update'] = category_to_update

    context["categories"] = Category.objects.all()
    
    context['value_to_update'] = value_to_update
    context['values'] = Value.objects.filter(category_id = category_to_update)
    context["answer_title_values"] = f"Categoría seleccionada: {category_to_update.name}"
    context["name_value_edition"] = True
    return render_login_required(request, template, context)

def articles_value_update_name(request, val_id, art_id=None):

    template = 'articles_category_value_section.html'

    context={}
    new_name = request.POST['value_name_update'].strip().title()
    value_to_update = Value.objects.get(id = val_id)
    context, is_empty_name_bool = is_empty_name(new_name, context)
    context, name_already_in_db_bool = name_already_in_db(new_name, Value, context)
    context, is_the_same_name_bool = is_the_same_name(new_name, value_to_update.name, context)


    category_to_update = Category.objects.get(id = value_to_update.category_id.id)
    context['category_to_update'] = category_to_update

    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['articles_any'] = [article_to_update]
    
    if is_the_same_name_bool == False and is_empty_name_bool == False and name_already_in_db_bool == False:
        context['answer'] = f'Se ha actualizado correctamente el valor {value_to_update.name} --> {new_name}!'
        value_to_update.name = new_name
        value_to_update.save()
    else:
        context['answer'] = f'No se puede actualizar el nombre del valor {value_to_update.name} --> {new_name}!'

    context['value_to_update'] = value_to_update
    context["categories"] = Category.objects.all()
    context['values'] = Value.objects.filter(category_id = category_to_update)
    context["answer_title_values"] = f"Categoría seleccionada: {category_to_update.name}"
    context["name_value_edition"] = False

    return render_login_required(request, template, context)

def customers(request):

    template="customers.html"

    customers = Customer.objects.all()

    answer = "Clientes en la Base de datos"
    context = {
                "customers_any": customers,
                "answer":answer,
                "datatype_input": 'name',
                "datatype": 'Nombre'
               }

    return render_login_required(request, template, context)

def customers_read_datatype(request):

    template = 'customers_search_datatype.html'
    context = {}
    datatype_input = request.GET['datatype_input'].strip()

    context.update(get_customers_by_native_datatype(datatype_input))

    return render_login_required(request, template, context)

def customers_read_data(request):

    template = "customers_search_right.html"

    search_input = request.GET["search_input"].strip()
    datatype_input = request.GET["datatype_input"].strip()
    context = {}

    if string_is_empty(search_input):
        """Si el campo de búsqueda está vacío se mostrarán todos los artículos"""
        context["articles_any"] = Customer.objects.all()

    else:
        """Si el campo de búsqueda no está vacío, se buscará de acuerdo a un tipo de dato nativo, (no categoría)"""
        context.update(get_customers_for_search_input_in_native_datatype(datatype_input, search_input))

    return render_login_required(request, template, context)
def customers_create(request):
    template = 'customers_search_right.html'
    context = {}
    return render_login_required(request, template, context)