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
        context["value"] = search_input
        if datatype_input == "id":
            context["articles_any"] = Article.objects.filter(id=search_input)
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
def articles_delete(request, id):

    context = {}

    try:

        articles_to_delete = get_object_or_404(Article, id=id)

    except Exception as e:
        context["articles_to_delete"] = articles_to_delete
        template = "articles_delete_error.html"
        return render_login_required(request, template, context)
    
    else:
        context["articles_deleted_name"] = articles_to_delete.articles_name
        articles_to_delete.delete() 

        template = "articles_delete_right.html"
        answer = "Artículos en la Base de datos"

        articles = Article.objects.all()

        context.update({"articles_all":articles,
                   "articles_any": articles,
                   "answer":answer,
                   })
        
        return render_login_required(request, template, context)

@csrf_protect
def articles_update(request, id):
    pass
    # """Show update form for the articles chosed """

    # articles_to_update = get_object_or_404(Articles, id=id)

    # context={}

    # categorie = Categorie.objects.all()
    # colors = Colors.objects.all()
    # materials = Materials.objects.all()
    # sizes = Sizes.objects.all()
    
    
    # articles_category_object = articles_to_update.category_id
    # articles_color_object = articles_to_update.color_id
    # articles_material_object = articles_to_update.material_id
    # articles_size_object = articles_to_update.size_id

    # articles_category_input = articles_category_object.id

    # try:
    #     articles_color_input = articles_color_object.id
    # except:
    #     articles_color_input = 'Empty'

    # try:
    #     articles_material_input = articles_material_object.id
    # except:
    #     articles_material_input = 'Empty'
        
    # try:
    #     articles_size_input = articles_size_object.id
    # except:
    #     articles_size_input = 'Empty'

    

    # context.update({"articles_category_input":articles_category_input,
    #                 "articles_color_input":articles_color_input,
    #                 "articles_material_input":articles_material_input,
    #                 "articles_size_input":articles_size_input})
    # context.update({"categorie":categorie,
    #                 "colors":colors,
    #                 "materials":materials,
    #                 "sizes":sizes})
    # context.update({"articles_to_update":articles_to_update})

    # buy_price = str(articles_to_update.buy_price).replace(",",".")
    # increase = str(articles_to_update.increase).replace(",",".")
    # sell_price = articles_to_update.sell_price

    # context["articles_buy_price_input"] = buy_price
    # context["articles_increase_input"] = increase
    # context["articles_sell_price_input"] = sell_price

    # template='articles_update.html'

    # return render_login_required(request, template, context)
    
# def articles_update_name_check(request, id):

#     context = {}

#     articles_to_update = get_object_or_404(Articles, id=id)
#     context.update({"articles_to_update":articles_to_update})

#     articles_name_input = request.GET['articles_name_input']
#     template = "articles_create_name_error.html"
#     context.update(name_check(articles_name_input))
#     return render_login_required(request, template, context)

# def articles_update_category_check(request, id):
    
    
#     context = {}

#     articles_to_update = get_object_or_404(Articles, id=id)
#     context.update({"articles_to_update":articles_to_update})

#     articles_category_input = request.GET['articles_category_input']
#     context.update(category_check(articles_category_input, context))
#     template = "articles_create_category_error.html"
#     return render_login_required(request, template, context)

# def articles_update_calculator(request, id):

#     context = {}

#     articles_to_update = get_object_or_404(Articles, id=id)
#     context.update({"articles_to_update":articles_to_update})

#     buy_price = request.GET['articles_buy_price_input']
#     increase = request.GET['articles_increase_input']
#     error_any = False

#     if is_empty(increase) or is_empty(buy_price):

#         error_any = True
#         context["answer_empty_error"] = "Debes completar los campos para calcular el precio de venta"

#     if not buy_price.replace(".","0",1).isnumeric() or  not increase.replace(".","0",1).isnumeric():
#         error_any = True
#         context["answer_string_error"] = "Los datos ingresados deben ser numéricos"
        
#     if error_any:
#         "show any error"
#         template = "articles_create_calculator_error.html"
#         return render_login_required(request, template, context)
    
#     else:

        
            
#         buy_price_float = float(buy_price)
#         increase_float = float(increase)
#         calculator = buy_price_float + ((buy_price_float * increase_float) / 100)
#         context["answer_calculator"] = calculator
#         template = "articles_create_calculator_right.html"

#     return render_login_required(request, template, context)

# def articles_update_confirm(request, id):
      
#     any_error = False
#     context = {}

#     articles_to_update = get_object_or_404(Articles, id=id)
    
#     articles_name_input = request.GET["articles_name_input"]
#     articles_category_input = request.GET['articles_category_input']
#     articles_color_input = request.GET['articles_color_input']
#     articles_material_input = request.GET['articles_material_input']
#     articles_size_input = request.GET['articles_size_input']
#     articles_buy_price_input = request.GET['articles_buy_price_input']
#     articles_increase_input = request.GET['articles_increase_input']
#     articles_sell_price_input = request.GET['articles_sell_price_input']
    
#     context.update({
#     "articles_name_input": articles_name_input,
#     "articles_category_input": str_to_int_if_possible(articles_category_input),
#     "articles_color_input":str_to_int_if_possible(articles_color_input),
#     "articles_material_input":str_to_int_if_possible(articles_material_input),
#     "articles_size_input":str_to_int_if_possible(articles_size_input),
#     "articles_buy_price_input":articles_buy_price_input,
#     "articles_increase_input":articles_increase_input,
#     "articles_sell_price_input":articles_sell_price_input,
#             })

#     # conditions to save
#     any_error, context = search_any_error(articles_name_input, articles_category_input, articles_sell_price_input, context)
#     # end of conditions to save 

#     categorie = Categorie.objects.all()
#     colors = Colors.objects.all()
#     materials = Materials.objects.all()
#     sizes = Sizes.objects.all()

#     context.update({
#         "categorie":categorie,
#         "colors":colors,
#         "materials":materials,
#         "sizes":sizes
#         })
    
#     if any_error == True:

#         # for render error answers
#         template = 'articles_update_save_error.html'
#         context["answer_save_error"] = "No se ha actualizado el artículo."
#         return render_login_required(request, template, context)
    
#     else:
#         objects = get_objects(articles_category_input,articles_color_input,articles_material_input,articles_size_input)

#         articles_to_update.articles_name = title(articles_name_input)
#         articles_to_update.category_id = objects["articles_category_object"]
#         articles_to_update.color_id = objects["articles_color_object"]
#         articles_to_update.material_id = objects["articles_material_object"]
#         articles_to_update.size_id = objects["articles_size_object"]
#         articles_to_update.buy_price = float(articles_buy_price_input)
#         articles_to_update.increase = float(articles_increase_input)
#         articles_to_update.sell_price = float(articles_sell_price_input.replace(',','.'))

#         articles_to_update.save()
        
#         context["articles_to_update"] = get_object_or_404(Articles, id=id)

#         template = "articles_update_save_right.html"
        
#         context["answer_articles_name"] = ""
#         context["answer_category_id"] = ""
#         context["answer_sell_price"] = ""
#         return render_login_required(request, template, context)
# ## Articles Categorie SECTION
def articles_categories(request):
    template = "categorie.html"
    categorie = Category.objects.all()
    context = {"categorie": categorie}
    return render_login_required(request, template, context)

# ## Articles Categorie Create
# def articles_categorie_save(request):

    
#     categorie = Categorie.objects.all()
#     category_input = request.GET['category_input']
#     context = {"category_input": category_input, "categorie": categorie}
    
#     if category_input == "":

#         template = "categorie_table_empty_error.html"
#         return render_login_required(request, template, context)
    
#     else:

#         try:

#             object = Categorie(category_name = category_input)
#             object.save()
#             template = "categorie_table_right.html"
#             return render_login_required(request, template, context)
#         except Exception as e:
#             print("-"*100)
#             print(f"ESTE ES EL ERROR -----------> {e.__str__} ")
#             print("-"*100)
#             template = "categorie_table_duplicate_error.html"
#             return render_login_required(request, template, context)

# def articles_categorie_update(request, id):

#     pass

# def articles_categorie_delete(request, id):

#     category_to_delete = get_object_or_404(Categorie, id = id)
#     context = {}
#     context["category_deleted_name"] = category_to_delete.category_name
#     category_to_delete.delete()
#     template = "categorie_delete_right.html"

#     categorie = Categorie.objects.all()
#     context["categorie"] = categorie

#     return render_login_required(request, template, context)

# ## Articles colors SECTION
# def articles_colors(request):
#     template = "colors.html"
#     colors = Colors.objects.all()
#     context = {"colors": colors}
#     return render_login_required(request, template, context)

# ## Articles colors create
# def articles_colors_save(request):

    
#     colors = Colors.objects.all()
#     color_input = request.GET['color_input']
#     context = {"color_input": color_input, "colors": colors}
    
#     if color_input == "":

#         template = "colors_table_empty_error.html"
#         return render_login_required(request, template, context)
    
#     else:

#         try:

#             object = Colors(color_name = color_input)
#             object.save()
#             template = "colors_table_right.html"
#             return render_login_required(request, template, context)
        
#         except Exception as e:
            
#             print("-"*100)
#             print(f"ESTE ES EL ERROR -----------> {e.__str__} ")
#             print("-"*100)
#             template = "colors_table_duplicate_error.html"
#             return render_login_required(request, template, context)
        
# def articles_colors_update(request, id):
#     pass

# def articles_colors_delete(request, id):

#     color_to_delete = get_object_or_404(Colors, id = id)
#     context = {}
#     context["color_deleted_name"] = color_to_delete.color_name
#     template = "colors_delete_right.html"
#     colors = Colors.objects.all()
#     context["colors"] = colors
    
#     try:

#         color_to_delete.delete()

#     except Exception as e:

#         print("-"*10,f"{e}","-"*10)
#         articles = Articles.objects.filter(color_id = color_to_delete)
#         print(articles,"*"*100)
#         context["articles_any"] = articles

#         if articles:

#             for articles in articles:

#                 articles.color_id = None
#                 articles.save()

#         color_to_delete.delete()

#     return render_login_required(request, template, context)

# ## Articles materials SECTION
# def articles_materials(request):

#     template = "materials.html"
#     materials = Materials.objects.all()
#     context = {"materials": materials}
#     return render_login_required(request, template, context)

# ## Articles materials create
# def articles_materials_save(request):

    
#     materials = Materials.objects.all()
#     material_input = request.GET['material_input']
#     context = {"material_input": material_input, "materials": materials}
    
#     if material_input == "":

#         template = "materials_table_empty_error.html"
#         return render_login_required(request, template, context)
    
#     else:

#         try:

#             object = Materials(material_name = material_input)
#             object.save()
#             template = "materials_table_right.html"
#             return render_login_required(request, template, context)
#         except Exception as e:
#             print("-"*100)
#             print(f"ESTE ES EL ERROR -----------> {e.__str__} ")
#             print("-"*100)
#             template = "materials_table_duplicate_error.html"
#             return render_login_required(request, template, context)
        
# def articles_materials_update(request, id):
#     pass

# def articles_materials_delete(request, id):

#     material_to_delete = get_object_or_404(Materials, id = id)
#     context = {}
#     context["material_deleted_name"] = material_to_delete.color_name
#     template = "materials_delete_right.html"
#     materials = Materials.objects.all()
#     context["materials"] = materials

#     material_to_delete.delete()

#     return render_login_required(request, template, context)

# ## Articles sizes SECTION

# def articles_sizes(request):
#     template = "sizes.html"
#     sizes = Sizes.objects.all()
#     context = {"sizes": sizes}
#     return render_login_required(request, template, context)

# ## Articles sizes create
# def articles_sizes_save(request):

    
#     sizes = Sizes.objects.all()
#     size_input = request.GET['size_input']
#     context = {"size_input": size_input, "sizes": sizes}
    
#     if size_input == "":

#         template = "sizes_table_empty_error.html"
#         return render_login_required(request, template, context)
    
#     else:

#         try:

#             object = Sizes(size_name = size_input)
#             object.save()
#             template = "sizes_table_right.html"
#             return render_login_required(request, template, context)
#         except Exception as e:
#             print("-"*100)
#             print(f"ESTE ES EL ERROR -----------> {e.__str__} ")
#             print("-"*100)
#             template = "sizes_table_duplicate_error.html"
#             return render_login_required(request, template, context)
        
# def articles_sizes_update(request, id):
#     pass

# def articles_sizes_delete(request, id):

#     size_to_delete = get_object_or_404(Sizes, id = id)
#     context = {}
#     context["size_deleted_name"] = size_to_delete.size_name
#     template = "sizes_delete_right.html"
#     sizes = Sizes.objects.all()
#     context["sizes"] = sizes

#     size_to_delete.delete()

#     return render_login_required(request, template, context)

# CUSTOMER SECTION

def customers(request):
    template="customers.html"
    return render_login_required(request, template,context={})