from django.shortcuts import render, get_object_or_404, redirect
from articles.models import Categories, Values, Articles, ArticlesValues, Customers, Stocks, Promotions, Orders, Expenses
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from .utils import *



# # ORDERS SECTION
def orders(request):
    return render_login_required(request, template_name="orders.html",context={})

# # ARTICLES SECTION

def articles(request):

    answer = "Artículos en la Base de datos"
    
    articles = Articles.objects.all()
    articles_values = ArticlesValues.objects.all()
    categories = Categories.objects.all()
    

    context = {
                "articles_any": articles,
                "answer":answer,
                "categories": categories,
                "articles_values": articles_values
               }
    template = "articles.html"
    return render_login_required(request, template, context)

### Articles read
def articles_read(request):
    
    context = {}
    
    datatype_dict = {
                    1: "id",
                    2: "name",
                    3: "buy_price",
                    4: "increase",
                    5: "sell_price"
                    }

    context["articles_any"] = Articles.objects.all()
    context["categories"] = Categories.objects.all()
    context["articles_values"] = ArticlesValues.objects.all()
    datatype_input = request.GET['datatype_input']
    template = "articles_search_datatype.html"
    if datatype_input == datatype_dict[1]:

        context["datatype_input"] = datatype_input
        context["datatype"] = "Id"

    elif datatype_input == datatype_dict[2]:

        context["datatype_input"] = datatype_input
        context["datatype"] = "Nombre"
        
    elif datatype_input == datatype_dict[3]:

        context["datatype_input"] = datatype_input
        context["datatype"] = "Precio de compra"

    elif datatype_input == datatype_dict[4]:

        context["datatype_input"] = datatype_input
        context["datatype"] = "Incremento"

    else: #datatype_input == datatype_dict[5]:

        context["datatype_input"] = datatype_input
        context["datatype"] = "Precio de venta"


    return render_login_required(request,template,context)

def articles_read_id(request):

    context = {}

    search_input = request.GET["search_input"]
    context["search_input"] = search_input
    context["datatype_input"] = "id"
    context["datatype"] = "Id"
    template = "articles_search_right.html"
        
    context["categories"] = Categories.objects.all()
    context["articles_values"] = ArticlesValues.objects.all()

    if is_empty(search_input):
        context["articles_any"] = Articles.objects.all()
        
    else:
        context["articles_any"] = Articles.objects.filter(id=search_input)

    return render_login_required(request, template, context)
 
def articles_read_name(request):

    context = {}

    search_input = request.GET["search_input"]
    
    context["search_input"] = search_input
    context["datatype_input"] = "name"
    context["categories"] = Categories.objects.all()
    context["articles_values"] = ArticlesValues.objects.all()
    context["datatype"] = "Nombre"

    template = "articles_search_right.html"

    if is_empty(search_input):
        print("EMPTY"*100)
        context["articles_any"] = Articles.objects.all()
    else:
        print("FULL"*100)
        context["articles_any"] = Articles.objects.filter(name__startswith=search_input)

    return render_login_required(request, template, context)

def articles_read_values(request):

    pass
def articles_read_buy_price(request):

    context = {}

    search_input = request.GET["search_input"]
    context["search_input"] = search_input
    context["datatype_input"] = "buy_price"
    context["categories"] = Categories.objects.all()
    context["articles_values"] = ArticlesValues.objects.all()
    context["datatype"] = "Precio de compra:"

    if is_empty(search_input):
        context["articles_any"] = Articles.objects.all()
    else:
        context["articles_any"] = Articles.objects.filter(buy_price__startswith=search_input)

    template = "articles_search_right.html"
    return render_login_required(request, template, context)
 
def articles_read_increase(request):

    context = {}

    search_input = request.GET["search_input"]
    context["search_input"] = search_input
    context["datatype_input"] = "increase"
    context["categories"] = Categories.objects.all()
    context["articles_values"] = ArticlesValues.objects.all()
    context["datatype"] = Articles.increase

    if is_empty(search_input):
        context["articles_any"] = Articles.objects.all()
    else:
        context["articles_any"] = Articles.objects.filter(increase__startswith=search_input)

    template = "articles_search_right.html"
    return render_login_required(request, template, context)
 
def articles_read_sell_price(request):

    context = {}
    context["categories"] = Categories.objects.all()
    context["articles_values"] = ArticlesValues.objects.all()
    context["datatype_input"] = "sell_price"

    search_input = request.GET["search_input"]
    context["search_input"] = search_input
    
    template = "articles_search_right.html"

    if is_empty(search_input):
        context["articles_any"] = Articles.objects.all()
    else:
        context["articles_any"] = Articles.objects.filter(sell_price__startswith=search_input)

    
    return render_login_required(request, template, context)

### Articles create
def articles_create(request):

    categories = Categories.objects.all()
    # colors = Colors.objects.all()
    # materials = Materials.objects.all()
    # sizes = Sizes.objects.all()
    context = {"categories":categories,
            #    "colors":colors,
            #    "materials":materials,
            #    "sizes":sizes
               }
    template='articles_create.html'

    return render_login_required(request, template, context)

# def articles_create_name_check(request):

#     context = {}
#     article_name_input = request.GET['article_name_input']
#     template = "articles_create_name_error.html"
#     context.update(name_check(article_name_input))
#     return render_login_required(request, template, context)

# def articles_create_category_check(request):
    
#     context = {}
#     article_category_input = request.GET['article_category_input']
#     context.update(category_check(article_category_input, context))
#     template = "articles_create_category_error.html"
#     return render_login_required(request, template, context)
    
# def articles_create_calculator(request):
#     context = {}
#     buy_price = request.GET['article_buy_price_input']
#     increase = request.GET['article_increase_input']
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
    
# def articles_create_confirm(request):
      
#     any_error = False
#     context = {}

#     article_name_input = request.GET["article_name_input"]
#     article_category_input = request.GET['article_category_input']
#     article_color_input = request.GET['article_color_input']
#     article_material_input = request.GET['article_material_input']
#     article_size_input = request.GET['article_size_input']
#     article_buy_price_input = request.GET['article_buy_price_input']
#     article_increase_input = request.GET['article_increase_input']
#     article_sell_price_input = request.GET['article_sell_price_input']

#     context.update({
#         "article_name_input": article_name_input,
#         "article_category_input": str_to_int_if_possible(article_category_input),
#         "article_color_input":str_to_int_if_possible(article_color_input),
#         "article_material_input":str_to_int_if_possible(article_material_input),
#         "article_size_input":str_to_int_if_possible(article_size_input),
#         "article_buy_price_input":article_buy_price_input,
#         "article_increase_input":article_increase_input,
#         "article_sell_price_input":article_sell_price_input,
#                 })
    
#     # conditions to save
#     any_error, context = search_any_error(article_name_input, article_category_input, article_sell_price_input, context)
    
#     categories = Categories.objects.all()
#     materials = Materials.objects.all()
#     colors = Colors.objects.all()
#     sizes = Sizes.objects.all()

#     context.update({
#             "categories":categories,
#             "materials":materials,
#             "colors":colors,
#             "sizes":sizes,
#         })
    
#     # end of conditions to save 
#     if any_error == True:

#         # for render error answers
#         template = 'articles_create_save_error.html'
#         context["answer_save_error"] = "No se ha creado el artículo."
#         return render_login_required(request, template, context)
    
#     else:

#         objects = get_objects(article_category_input,article_color_input,article_material_input,article_size_input)

#         article = Articles(
#             article_name = title(article_name_input),
#             category_id = objects["article_category_object"],
#             color_id = objects["article_color_object"],
#             material_id = objects["article_material_object"],
#             size_id = objects["article_size_object"], 
#             buy_price = float(article_buy_price_input), 
#             increase = float(article_increase_input),
#             sell_price = float(article_sell_price_input.replace(',', '.'))
#             )

#         article.save()

#         template = "articles_create_save_right.html"

#         context["answer_save_right"] = f"El artículo {article.article_name} se ha guardado correctamente"
#         context["answer_article_name"] = ""
#         context["answer_category_id"] = ""
#         context["answer_sell_price"] = ""

#         return render_login_required(request, template, context)

#Articles delete ##REVISAR EL CONTEXTO
@csrf_protect
def articles_delete(request, id):

    context = {}

    try:

        article_to_delete = get_object_or_404(Articles, id=id)

    except Exception as e:
        context["article_to_delete"] = article_to_delete
        template = "articles_delete_error.html"
        return render_login_required(request, template, context)
    
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
        
        return render_login_required(request, template, context)

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

    return render_login_required(request, template, context)
    
# def articles_update_name_check(request, id):

#     context = {}

#     article_to_update = get_object_or_404(Articles, id=id)
#     context.update({"article_to_update":article_to_update})

#     article_name_input = request.GET['article_name_input']
#     template = "articles_create_name_error.html"
#     context.update(name_check(article_name_input))
#     return render_login_required(request, template, context)

# def articles_update_category_check(request, id):
    
    
#     context = {}

#     article_to_update = get_object_or_404(Articles, id=id)
#     context.update({"article_to_update":article_to_update})

#     article_category_input = request.GET['article_category_input']
#     context.update(category_check(article_category_input, context))
#     template = "articles_create_category_error.html"
#     return render_login_required(request, template, context)

# def articles_update_calculator(request, id):

#     context = {}

#     article_to_update = get_object_or_404(Articles, id=id)
#     context.update({"article_to_update":article_to_update})

#     buy_price = request.GET['article_buy_price_input']
#     increase = request.GET['article_increase_input']
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

#     article_to_update = get_object_or_404(Articles, id=id)
    
#     article_name_input = request.GET["article_name_input"]
#     article_category_input = request.GET['article_category_input']
#     article_color_input = request.GET['article_color_input']
#     article_material_input = request.GET['article_material_input']
#     article_size_input = request.GET['article_size_input']
#     article_buy_price_input = request.GET['article_buy_price_input']
#     article_increase_input = request.GET['article_increase_input']
#     article_sell_price_input = request.GET['article_sell_price_input']
    
#     context.update({
#     "article_name_input": article_name_input,
#     "article_category_input": str_to_int_if_possible(article_category_input),
#     "article_color_input":str_to_int_if_possible(article_color_input),
#     "article_material_input":str_to_int_if_possible(article_material_input),
#     "article_size_input":str_to_int_if_possible(article_size_input),
#     "article_buy_price_input":article_buy_price_input,
#     "article_increase_input":article_increase_input,
#     "article_sell_price_input":article_sell_price_input,
#             })

#     # conditions to save
#     any_error, context = search_any_error(article_name_input, article_category_input, article_sell_price_input, context)
#     # end of conditions to save 

#     categories = Categories.objects.all()
#     colors = Colors.objects.all()
#     materials = Materials.objects.all()
#     sizes = Sizes.objects.all()

#     context.update({
#         "categories":categories,
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
#         objects = get_objects(article_category_input,article_color_input,article_material_input,article_size_input)

#         article_to_update.article_name = title(article_name_input)
#         article_to_update.category_id = objects["article_category_object"]
#         article_to_update.color_id = objects["article_color_object"]
#         article_to_update.material_id = objects["article_material_object"]
#         article_to_update.size_id = objects["article_size_object"]
#         article_to_update.buy_price = float(article_buy_price_input)
#         article_to_update.increase = float(article_increase_input)
#         article_to_update.sell_price = float(article_sell_price_input.replace(',','.'))

#         article_to_update.save()
        
#         context["article_to_update"] = get_object_or_404(Articles, id=id)

#         template = "articles_update_save_right.html"
        
#         context["answer_article_name"] = ""
#         context["answer_category_id"] = ""
#         context["answer_sell_price"] = ""
#         return render_login_required(request, template, context)
# ## Articles Categories SECTION
def articles_categories(request):
    template = "categories.html"
    categories = Categories.objects.all()
    context = {"categories": categories}
    return render_login_required(request, template, context)

# ## Articles Categories Create
# def articles_categories_save(request):

    
#     categories = Categories.objects.all()
#     category_input = request.GET['category_input']
#     context = {"category_input": category_input, "categories": categories}
    
#     if category_input == "":

#         template = "categories_table_empty_error.html"
#         return render_login_required(request, template, context)
    
#     else:

#         try:

#             object = Categories(category_name = category_input)
#             object.save()
#             template = "categories_table_right.html"
#             return render_login_required(request, template, context)
#         except Exception as e:
#             print("-"*100)
#             print(f"ESTE ES EL ERROR -----------> {e.__str__} ")
#             print("-"*100)
#             template = "categories_table_duplicate_error.html"
#             return render_login_required(request, template, context)

# def articles_categories_update(request, id):

#     pass

# def articles_categories_delete(request, id):

#     category_to_delete = get_object_or_404(Categories, id = id)
#     context = {}
#     context["category_deleted_name"] = category_to_delete.category_name
#     category_to_delete.delete()
#     template = "categories_delete_right.html"

#     categories = Categories.objects.all()
#     context["categories"] = categories

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

#             for article in articles:

#                 article.color_id = None
#                 article.save()

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

# CUSTOMERS SECTION

def customers(request):
    return render_login_required(request, template_name="customers.html",context={})