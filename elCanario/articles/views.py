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
    
    answer = "Articles in Database"
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
        """checks that the user's selection is a category"""

        if string_is_empty(search_input):
            """fetches all items containing values in that category"""
            context.update(get_articles_by_category_datatype(datatype_input))

        else:
            """brings all items that have that specific value"""
            context.update(get_articles_for_value_of_category(datatype_input,search_input))

    else:
        """the user has selected as search type a native data type, (no category)"""

        if string_is_empty(search_input):
            """If the search field is empty, all items will be displayed."""
            context["articles_any"] = Article.objects.all()

        else:
            """If the search field is not empty, it will be searched according to a native data type (not category)."""
            context.update(get_articles_for_search_input_in_native_datatype(datatype_input, search_input))
        
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
    context, any_error = search_any_error_in_name_field(article_name_input, context)
    context, any_error = name_already_in_db(article_name_input, Article, context)
    return render_login_required(request, template, context)

def articles_update_name_check(request, id):

    template = "articles_create_name_error.html"
    
    context = {}
    article_name_input = request.GET['article_name_input'].strip().title()
    article_to_update = Article.objects.get(id=id)
    
    if not article_name_input == article_to_update.name:
        context, any_error = search_any_error_in_name_field(article_name_input,context)
        context, any_error = name_already_in_db(article_name_input, Article, context)
    context["article_to_update"] = article_to_update
    return render_login_required(request, template, context)

def articles_create_calculator(request):

    template = "articles_create_calculator.html"


    context = {}
    buy_price = request.GET['article_buy_price_input'].replace(',', '.')
    increase = request.GET['article_increase_input'].replace(',', '.')
    any_error = False

    context, any_error = calculator_check(increase, buy_price, context)

    if any_error:
        """show any error"""
        return render_login_required(request, template, context)
    
    else:
        
        buy_price_float = float(buy_price)
        increase_float = float(increase)
        calculator = buy_price_float + ((buy_price_float * increase_float) / 100)
        context["answer_calculator"] = calculator
        
    return render_login_required(request, template, context)
    
def articles_create_confirm(request):

    template = 'articles_create_save.html'
      
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
        #if there is any error I must keep the values that were selected in each category.
        context.update(keep_selected_values(request))


    if any_error == True:

        # for render error answers
        context.update(values_dict)
        context["answer_save_error"] = "The item has not been created, please check the fields again."
        return render_login_required(request, template, context)

    else:

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

        context["answer_save_right"] = f"The article {article.name} has been saved correctly"
        context["answer_articles_name"] = ""
        context["answer_category_id"] = ""

        return render_login_required(request, template, context)

def articles_update_confirm(request, id):

    template = "articles_create_save.html"

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

        # for render error answer
        context.update(values_dict)
        context["answer_save_error"] = "The item has not been created, please check the fields again."
        context["article_to_update"] = article_to_update
        return render_login_required(request, template, context)

    else:
        
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

        context["answer_save_right"] = f"The article {article_to_update.name} has been successfully updated"
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
        
        context["article_delete_answer"] = f"The article {article_to_delete.name} was correctly deleted"
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
        context["answer_title_values"] = f"Add values to: {category_to_save.name}"
        context["answer"] = f"The category {category_to_save.name} has been successfully saved!"
    else:
        context["answer"] = "Category could not be saved!"

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
        context['answer'] = f'The value {value_name} was saved correctly for the category: {category_to_update.name}'
        context['values'] = Value.objects.filter(category_id = category_to_update)
    else:
        context["answer"] = f"The value {value_name} could not be saved for the category: {category_to_update.name}"
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
    context["answer_title_values"] = f"Selected category: {category_to_update.name}"
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
        context['answer'] = f'Category has been successfully updated {category_to_update.name} --> {new_name}!'
        category_to_update.name = new_name
        category_to_update.save()
    else:
        context['answer'] = f'Unable to update the category name {category_to_update.name} --> {new_name}!'

    context["categories"] = Category.objects.all()
    context['values'] = Value.objects.filter(category_id = category_to_update)
    context["answer_title_values"] = f"Selected category: {category_to_update.name}"
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
    context["answer"] = f"The category {category_to_update.name} has been eliminated."
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
    context["answer"] = f"The value {value_to_update.name} has been removed from the category {category_to_update.name}"
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
    context["answer_title_values"] = f"Selected category: {category_to_update.name}"
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
        context['answer'] = f'The value has been updated correctly: {value_to_update.name} --> {new_name}!'
        value_to_update.name = new_name
        value_to_update.save()
    else:
        context['answer'] = f'Unable to update the value name: {value_to_update.name} --> {new_name}!'

    context['value_to_update'] = value_to_update
    context["categories"] = Category.objects.all()
    context['values'] = Value.objects.filter(category_id = category_to_update)
    context["answer_title_values"] = f"Selected category: {category_to_update.name}"
    context["name_value_edition"] = False

    return render_login_required(request, template, context)

def customers(request):

    template="customers.html"

    customers = Customer.objects.all()

    answer = "Customers in Database"
    context = {
                "customers_any": customers,
                "answer":answer,
                "datatype_input": 'name',
                "datatype": 'Name'
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
        """If the search field is empty, all items will be displayed."""
        context["articles_any"] = Customer.objects.all()

    else:
        """If the search field is not empty, it will be searched according to a native data type (not category)."""
        context.update(get_customers_for_search_input_in_native_datatype(datatype_input, search_input))

    return render_login_required(request, template, context)
def customers_create(request):
    template = 'customers_search_right.html'
    context = {}
    return render_login_required(request, template, context)