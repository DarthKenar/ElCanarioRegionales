from logging import info
from typing import Any, Dict
from urllib import request
from articles.models import Article, ArticleValue, Category, Promotion, Value
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from articles.utils import *
from elCanario.utils import *


class ArticleListView(LoginRequiredMixin,ListView):
    """List all existing articles

    Args:
        LoginRequiredMixin: Allow access to the view for registered users only.
        ListView: ListView Generic

    Returns:
        HttpResponse: /read
    """
    model = Article
    template_name = 'articles.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context["datatype"] = _('Name')
        context["datatype_input"] = 'name'
        context["answer"] = _("Articles in Database")
        context["categories"] = categories
        return context


class ReadDataListView(LoginRequiredMixin, ListView):
    """Lists all existing articles that match the specific value entered/selected (Data).
    For example: Assuming that the Article Model has a "Name" attribute
    DataType: Name
    Data: Table

    Args:
        LoginRequiredMixin: Allow access to the view for registered users only.
        ListView: ListView Generic

    Returns:
        HttpResponse: /read_data
    """
    template_name = 'articles_search_data.html'
    model = Article

    def get_queryset(self) -> QuerySet[Any]:
        search_input = self.request.GET["search_input"].strip()
        datatype_input = self.request.GET["datatype_input"].strip()
        if datatype_input.isnumeric():
            if string_is_empty(search_input):
                category_selected = int(datatype_input)
                category = Category.objects.get(id = category_selected)
                return Article.objects.filter(characteristics_id__category_id=category)
            else:
                value = Value.objects.get(id = search_input)
                return Article.objects.filter(characteristics_id=value)
        else:
            if string_is_empty(search_input):
                return Article.objects.all()
            else:
                return get_articles_for_search_input_in_native_datatype(datatype_input, search_input)
                
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        search_input = self.request.GET["search_input"].strip()
        datatype_input = self.request.GET["datatype_input"].strip()
        context["search_input"] = search_input
        context["categories"] = Category.objects.all()
        if datatype_input.isnumeric():
            if string_is_empty(search_input):
                context.update(get_context_by_category(datatype_input))
            else:
                context.update(get_context_for_value_of_category(datatype_input,search_input))
        else:
            if string_is_empty(search_input):
                pass
            else:
                context.update(get_context_for_search_input_in_native_datatype(datatype_input, search_input))
        return context


class ReadDatatypeListView(LoginRequiredMixin, ListView):
    """Lists all existing Articles that match the selected Data Type, corresponding attribute of the Article model.
    For example: Assuming that the Article model has an attribute "Name
    Data Type: Name
    Data: ...

    Args:
        LoginRequiredMixin: Allow access to the view only to registered users.
        ListView: Generic ListView

    Returns:
        HttpResponse: /read_datatype
    """
    template_name = 'articles_search_datatype.html'
    model = Article
    
    def get_queryset(self) -> QuerySet[Any]:
        category_selected = self.request.GET['datatype_input'].strip()
        if category_selected.isnumeric():
            category = Category.objects.get(id = category_selected)
            return Article.objects.filter(characteristics_id__category_id=category)
        else:
            return Article.objects.all()

    def get_context_data(self, **kwargs):
        datatype_input = self.request.GET['datatype_input'].strip()
        context = super().get_context_data(**kwargs)
        if datatype_input.isnumeric():
            # if numeric, the user has selected some category as data type
            context.update(get_context_by_category(datatype_input))
        else:
            # if not numeric, the user has selected some article native field as data type
            context.update(get_articles_by_native_datatype(datatype_input))
        return context


class ArticleCreateView(LoginRequiredMixin, TemplateView):
    """Redirects the user to create an Article in case you use the GET method, if you use the POST method it is assumed that you are already in the form checking the fields and saving the article if possible.

    Args:
        LoginRequiredMixin: Allow access to the view for registered users only.
        CreateView: CreateView Generic

    Returns:
        HttpResponse: 
            GET: Redirects to the creation form
            POST: A portion of the html is replaced using htmx  
    """
    template_name = 'articles_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        values = Value.objects.all()
        context = {"categories":categories,
                   "values":values}
        return context

def articles_create_name_check(request):
    """Check that the name is correct (go through the validators) and add the errors to the context if there are any
    (validators for create name)

    Args:
        request (HttpRequest): request

    Returns:
        render_login_required (function): render_login_required
    """
    template = "articles_create_name_error.html"
    context = {}
    article_name_input = request.GET['article_name_input'].strip().title()
    context, any_error = search_any_error_in_name_field(article_name_input, context)
    context, any_error = name_already_in_db(article_name_input, Article, context)
    return render_login_required(request, template, context)

def articles_update_name_check(request, pk):
    """Check that the name is correct (go through the validators) and add the errors to the context if there are any
    (validators for update name)

    Args:
        request (HttpRequest): request

    Returns:
        render_login_required (function): render_login_required
    """
    template = "articles_create_name_error.html"
    context = {}
    article_name_input = request.GET['article_name_input'].strip().title()
    article_to_update = Article.objects.get(id=pk)
    if not article_name_input == article_to_update.name:
        context, any_error = search_any_error_in_name_field(article_name_input,context)
        context, any_error = name_already_in_db(article_name_input, Article, context)
    context["article_to_update"] = article_to_update
    return render_login_required(request, template, context)

def articles_create_calculator(request):
    """Creates the sell_price according to the purchase price and the increment and adds to the context the errors if any

    Args:
        request (HttpRequest): request

    Returns:
        render_login_required (function): render_login_required
    """

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

def create_stock_check(request):
    """Checks for errors in the Stock field and adds the answers to the context if there are any errors.

    Args:
        request (HttpRequest): request
 
    Returns:
        render_login_required (function): render_login_required
    """
    template = "articles_create_stock_check.html"
    stock_input:str = request.GET['article_stock_input']
    context:dict = {}
    context, any_error = search_any_error_in_stock_field(stock_input,context)
    return render_login_required(request, template, context)

def articles_create_confirm(request):
    """Checks that there are no errors in all fields, saves the item and adds a successful response if there are no errors, otherwise if there are errors it does not save the article and adds to the context responses to the errors.
    

    Args:
        request (HttpRequest): request

    Returns:
        render_login_required (function): render_login_required
    """
    template = 'articles_create_save.html'
    any_error = False
    context = {}
    categories = Category.objects.all()
    values = Value.objects.all()
    context["categories"] = categories
    context["values"] = values
    context["title"] = _("Create Article")
    article_name_input = request.GET["article_name_input"].strip().title()
    article_buy_price_input = request.GET['article_buy_price_input'].replace(',', '.')
    article_increase_input = request.GET['article_increase_input'].replace(',', '.')
    answer_calculator = request.GET['article_sell_price_input'].replace(',', '.')
    article_stock_input = request.GET['article_stock_input']
    context.update({
        "article_name_input": article_name_input,
        "article_buy_price_input":article_buy_price_input,
        "article_increase_input":article_increase_input,
        "answer_calculator":answer_calculator,
        "article_stock_input":article_stock_input,
                })
    # conditions to save
    error_context = {}
    error_context, search_any_error_in_name_field_bool = search_any_error_in_name_field(article_name_input, context)
    error_context, calculator_check_bool = calculator_check(article_increase_input,article_buy_price_input, context)
    error_context, name_already_in_db_bool = name_already_in_db(article_name_input, Article, context)
    error_context, search_any_error_in_stock_field_bool = search_any_error_in_stock_field(article_stock_input,context)
    values_dict = get_values_for_categories(request)
    # end of conditions to save 
    if search_any_error_in_name_field_bool == True or calculator_check_bool == True or name_already_in_db_bool == True or search_any_error_in_stock_field_bool == True:
        any_error = True
        context.update(error_context)
        #if there is any error I must keep the values that were selected in each category.
        context.update(keep_selected_values(request))
    if any_error == True:
        # for render error answers
        context.update(values_dict)
        context["answer_save_error"] = _("The item has not been created, please check the fields again.")
        return render_login_required(request, template, context)
    else:
        context.pop("article_name_input")
        context.pop("article_buy_price_input")
        context.pop("article_increase_input")
        context.pop("answer_calculator")
        context.pop("article_stock_input")
        article = Article(
            name = title(article_name_input),
            buy_price = float(article_buy_price_input), 
            increase = float(article_increase_input),
            sell_price = float(answer_calculator),
            stock = article_stock_input
            )
        article.save()
        for value in values_dict.values():
            if value != None:
                article_value = ArticleValue(
                                    article_id = article,
                                    category_id = value.category_id,
                                    value_id = value)
                article_value.save()
        context["answer_save_right"] = _(f"The article {article.name} has been saved correctly")
        context["answer_articles_name"] = ""
        context["answer_category_id"] = ""
        context["answer_error_name"] = ""
        return render_login_required(request, template, context)

def articles_update_confirm(request, id):
    """Checks that there are no errors in all fields, saves the item and adds a successful response if there are no errors, otherwise if there are errors it does not update the article and adds to the context responses to the errors.
    

    Args:
        request (HttpRequest): request

    Returns:
        render_login_required (function): render_login_required
    """
    template = "articles_create_save.html"
    any_error = False
    context = {}
    categories = Category.objects.all()
    values = Value.objects.all()
    article_to_update = Article.objects.get(id=id)
    context["categories"] = categories
    context["values"] = values
    context["title"] = _("Update Article")
    article_name_input = request.GET["article_name_input"].strip().title()
    article_buy_price_input = request.GET['article_buy_price_input'].replace(',', '.')
    article_increase_input = request.GET['article_increase_input'].replace(',', '.')
    answer_calculator = request.GET['article_sell_price_input'].replace(',', '.')
    article_stock_input = request.GET['article_stock_input']
    context.update({
        "article_name_input": article_name_input,
        "article_buy_price_input":article_buy_price_input,
        "article_increase_input":article_increase_input,
        "answer_calculator":answer_calculator,
        "article_stock_input":article_stock_input,})
    # conditions to save
    error_context = {}
    if not article_name_input == article_to_update.name:
        error_context, search_any_error_in_name_field_bool = search_any_error_in_name_field(article_name_input, context)
        error_context, name_already_in_db_bool = name_already_in_db(article_name_input, Article, context)
    error_context, calculator_check_bool = calculator_check(article_increase_input,article_buy_price_input, context)
    error_context, search_any_error_in_stock_field_bool = search_any_error_in_stock_field(article_stock_input,context)
    values_dict = get_values_for_categories(request)
    # end of conditions to save 
    if not article_name_input == article_to_update.name:
        if search_any_error_in_name_field_bool == True or calculator_check_bool == True or name_already_in_db_bool == True or search_any_error_in_stock_field_bool == True:
            any_error = True
            context.update(error_context)
    if any_error == True:
        # for render error answer
        context.update(values_dict)
        context["answer_save_error"] = _("The item has not been created, please check the fields again.")
        context["article_to_update"] = article_to_update
        return render_login_required(request, template, context)
    else:
        context.pop("article_name_input")
        context.pop("article_buy_price_input")
        context.pop("article_increase_input")
        context.pop("answer_calculator")
        context.pop("article_stock_input")
        article_to_update.name = article_name_input
        article_to_update.buy_price = article_buy_price_input
        article_to_update.increase = article_increase_input
        article_to_update.sell_price = answer_calculator
        article_to_update.stock = article_stock_input
        article_to_update.save()
        delete_old_values(article_to_update)
        for value in values_dict.values():
            if value != None:
                article_value = ArticleValue(
                                    article_id = article_to_update,
                                    category_id = value.category_id,
                                    value_id = value)
                article_value.save()
        context["answer_save_right"] = _(f"The article {article_to_update.name} has been successfully updated")
        context["answer_articles_name"] = ""
        context["answer_category_id"] = ""
        categories = Category.objects.all()
        values = Value.objects.all()
        context["categories"] = categories
        context["values"] = values
        return render(request, template, context)

@csrf_protect
def article_delete(request:HttpRequest, pk:int)-> HttpResponse:
    """View used for the deletion of an object of type Article.
    - Has crsf protection.
    - Login required.
    Args:
        request (HttpRequest): request
        pk (int): Identifier of the article to be deleted.

    Returns:
        HttpResponse: returns the list of all articles in context
    """
    template = 'articles_search_data.html'
    context = {}
    try:
        article_to_delete = get_object_or_404(Article, id=pk)
    except Exception as e:
        context["delete_answer"] = _(f"The selected article could not be deleted because it does not exist. Please contact Support")
        return render_login_required(request, template, context)
    else:
        context["delete_answer"] = _(f"The article {article_to_delete.name} has been eliminated")
        article_to_delete.delete()
        articles = Article.objects.all()
        context.update({"object_list": articles})
        return render_login_required(request, template, context)    
    
class ArticleDetailView(LoginRequiredMixin, DetailView):
    """Renders the template to update a specific article

    Args:
        LoginRequiredMixin: Allow access to the view for registered users only.
        DetailView: DetailView Generic

    Returns:
        HttpResponse: HttpResponse
    """
    model = Article
    template_name = 'articles_update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        pk = self.kwargs.get('pk')
        article_to_update = get_object_or_404(Article,pk=pk)
        values = Value.objects.all()
        context.update({"categories":categories,
                        "values":values,
                        "article_to_update":article_to_update})
        return context
    
#CATEGORIES

class CategoriesView(LoginRequiredMixin, TemplateView):
    """Render template to access the Categories section

    Args:
        LoginRequiredMixin: Allow access to the view for registered users only.
        TemplateView: TemplateView Generic

    Returns:
        HttpResponse: HttpResponse
    """
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
    

def articles_category_create(request, art_id:str=None):
    """Creates a new category in case there are no errors, if there are any, renders them by context

    Args:
        request (HttpRequest): request
        art_id (str, optional): There is an option to edit a category but send an article id by context to continue editing it.

    Returns:
        render_login_required (function): render_login_required
    """
    template = 'articles_category_value_section.html'
    category_name = request.POST["category_name_new"].strip().title()
    context = {}
    context["categories"] = Category.objects.all()
    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['article_list'] = [article_to_update]
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
        context["answer"] = _(f"The category {category_to_save.name} has been successfully saved!")
    else:
        context["answer"] = _("Category could not be saved!")

    return render_login_required(request, template, context)

def articles_category_value_create(request,cat_id:str, art_id:str=None):
    """Creates a new value for the category selected (cat_id) in case there are no errors, if there are any, renders them by context

    Args:
        request (HttpRequest): request
        cat_id (str): Category to which the value will be assigned
        art_id (str, optional): There is an option to edit a category but send an article id by context to continue editing it.

    Returns:
        render_login_required (function): render_login_required
    """
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
        context['article_list'] = [article_to_update]
    if name_already_in_db_bool == True or is_empty_name_bool == True:
        any_error = True
    if any_error == False:
        value_to_update = Value(
                            category_id = category_to_update,
                            name = value_name)
        value_to_update.save()
        context['answer'] = _(f'The value {value_name} was saved correctly for the category: {category_to_update.name}')
        context['values'] = Value.objects.filter(category_id = category_to_update)
    else:
        context["answer"] = _(f"The value {value_name} could not be saved for the category: {category_to_update.name}")
        context['values'] = Value.objects.filter(category_id = category_to_update)
    return render_login_required(request, template, context)

def articles_category_update(request: object, external_link: str, cat_id:int, art_id:str=None, cat_update_name:str=None) -> HttpResponse:
    """redirects to the categories section taking the article with it.
        This is done in order to update the data in the categories section and then be able to edit the article easily.

    Args:
        request (HttpRequest): request
        external_link (str): It is used to know if the editing of a category is selected from the same category section or not. This is used to know whether to render the whole template or a portion of it using htmx.
        cat_id (str): Selected category for editing
        art_id (str, optional): There is an option to edit a category but send an article id by context to continue editing it.

    Returns:
        HttpResponse: If the editing of the selected category is requested from a page external to the category section, the httpResponse template will be that of the category section and will add the category to be edited and the article from which it was selected to the context.
                    In case the edition is made from the same category section, it does not send the article from which the edition was requested and will return a partial template response.
    """

    external_link = true_or_false_str_to_bool(external_link)
    if external_link == False:
        template = "articles_category_value_section.html"
    else: 
        template = "categories.html"
    context={}
    category_to_update = Category.objects.get(id = cat_id)
    context['category_to_update'] = category_to_update
    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['article_list'] = [article_to_update]
    context["categories"] = Category.objects.all()
    context['values'] = Value.objects.filter(category_id = category_to_update)
    if cat_update_name == "True":
        context["name_category_edition"] = True
    return render_login_required(request, template, context)

def articles_category_update_name(request, cat_id, art_id=None):
    """Updates the category name if there are no errors, otherwise the errors are rendered by context.

    Args:
        request (HttpRequest): request
        cat_id (str): Selected category for update name
        art_id (str, optional): There is an option to edit a category but send an article id by context to continue editing it.

    Returns:
        render_login_required (function): render_login_required
    """
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
        context['article_list'] = [article_to_update]
    if search_any_error_in_name_field_bool == False and is_the_same_name_bool == False and name_already_in_db_bool == False:
        context['answer'] = _(f'Category has been successfully updated {category_to_update.name} --> {new_name}!')
        category_to_update.name = new_name
        category_to_update.save()
    else:
        context['answer'] = _(f'Unable to update the category name {category_to_update.name} --> {new_name}!')
    context["categories"] = Category.objects.all()
    context['values'] = Value.objects.filter(category_id = category_to_update)
    context["name_category_edition"] = False
    return render_login_required(request, template, context)
    
def articles_category_delete(request, cat_id: str, art_id:str=None):
    """ Deletes the selected cat_id category

    Args:
        request (HttpRequest): request
        cat_id (str): Category selected for deletion
        art_id (str, optional): There is an option to edit a category but send an article id by context to continue editing it.

    Returns:
        render_login_required (function): render_login_required
    """
    template = 'articles_category_value_section.html'
    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['article_list'] = [article_to_update]
    context={}
    category_to_update = Category.objects.get(id = cat_id)
    context["answer_delete"] = _(f"The category {category_to_update.name} has been eliminated.")
    category_to_update.delete()
    context["categories"] = Category.objects.all()
    return render_login_required(request, template, context)

def articles_value_delete(request, cat_id: str, val_id: str, art_id:str=None):
    """ Deletes the selected val_id value from cat_id category

    Args:
        request (HttpRequest): request
        cat_id (str): Category selected
        val_id (str): Value selected for deletion
        art_id (str, optional): There is an option to edit a category but send an article id by context to continue editing it.

    Returns:
        render_login_required (function): render_login_required
    """
    template = 'articles_category_value_section.html'
    context={}
    value_to_update = Value.objects.get(id = val_id)
    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['article_list'] = [article_to_update]
    category_to_update = Category.objects.get(id = cat_id)
    context['category_to_update'] = category_to_update
    context["answer"] = _(f"The value {value_to_update.name} has been removed from the category {category_to_update.name}")
    value_to_update.delete()
    context["categories"] = Category.objects.all()
    context['values'] = Value.objects.filter(category_id = category_to_update)
    return render_login_required(request, template, context)

def articles_value_update(request, cat_id, val_id, art_id=None):
    """ Enables editing of the selected value val_id of the selected category cat_id giving way to articles_value_update_name.

    Args:
        request (HttpRequest): request
        cat_id (str): Category selected
        val_id (str): Value selected
        art_id (str, optional): There is an option to edit a category but send an article id by context to continue editing it.

    Returns:
        render_login_required (function): render_login_required
    """
    context={}
    value_to_update = Value.objects.get(id = val_id)
    template = 'articles_category_value_section.html'
    if not string_is_empty(art_id):
        article_to_update = Article.objects.get(id = art_id)
        context['article_to_update'] = article_to_update
        context['article_list'] = [article_to_update]
    category_to_update = Category.objects.get(id = cat_id)
    context['category_to_update'] = category_to_update
    context["categories"] = Category.objects.all()
    context['value_to_update'] = value_to_update
    context['values'] = Value.objects.filter(category_id = category_to_update)
    context["name_value_edition"] = True
    return render_login_required(request, template, context)

def articles_value_update_name(request, val_id, art_id=None):
    """ Update the name of the selected category value

    Args:
        request (HttpRequest): request
        val_id (str): Value selected
        art_id (str, optional): There is an option to edit a category but send an article id by context to continue editing it.

    Returns:
        render_login_required (function): render_login_required
    """
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
        context['article_list'] = [article_to_update]
    if is_the_same_name_bool == False and is_empty_name_bool == False and name_already_in_db_bool == False:
        context['answer'] = _(f"A category value {value_to_update.category_id.name} has been successfully updated: Previous value name: {category_to_update.name}, New name {new_name}.")
        value_to_update.name = new_name
        value_to_update.save()
    else:
        context['answer'] = _(f'Unable to update the value name: {value_to_update.name} --to--> {new_name}!')
    context['value_to_update'] = value_to_update
    context["categories"] = Category.objects.all()
    context['values'] = Value.objects.filter(category_id = category_to_update)
    context["name_value_edition"] = False
    return render_login_required(request, template, context)