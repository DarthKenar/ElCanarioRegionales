from django.shortcuts import render
from articles.models import Articles, Categories, Colors, Sizes, Materials
from django.http import HttpResponse
# Create your views here.

##ORDERS SECTION
def section_orders(request):
    return render(request, template_name="orders.html",context={})

##CUSTOMERS SECTION
def section_customers(request):
    return render(request, template_name="customers.html",context={})


##ARTICLES SECTION
def section_articles_deliver(request, context: dict): 
    
    return render(request,"articles.html", context)

def section_articles(request):

    first_time_articles = request.GET['first_time_articles']
    
    if first_time_articles == '1':

        answer = "Artículos en la Base de datos"
        articles = Articles.objects.all()
        context = {"articles_all":articles, "articles_any": articles, "answer":answer}
        return section_articles_deliver(request, context)
    
    else:

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
                articles = Articles.objects.filter(id__icontains=article_input)
            elif datatype_input == datatype_dict[2]:
                datatype = "Nombre"
                articles = Articles.objects.filter(article_name__icontains=article_input)
            elif datatype_input == datatype_dict[3]:
                datatype = "Categoría"
                category_object = Categories.objects.filter(category_name__icontains=article_input)
                articles = Articles.objects.filter(category_id__in=category_object)
            elif datatype_input == datatype_dict[4]:
                datatype = "Color"
                color_object = Colors.objects.filter(color_name__icontains=article_input)
                articles = Articles.objects.filter(color_id__in=color_object)
            elif datatype_input == datatype_dict[5]:
                datatype = "Material"
                material_object = Materials.objects.filter(material_name__icontains=article_input)
                articles = Articles.objects.filter(material_id__in=material_object)
            elif datatype_input == datatype_dict[6]:
                datatype = "Talle/Tamaño"
                size_object = Sizes.objects.filter(size_name__icontains=article_input)
                articles = Articles.objects.filter(size_id__in=size_object)
            elif datatype_input == datatype_dict[7]:
                datatype = "Precio de compra"
                articles = Articles.objects.filter(buy_price__icontains=article_input)
            elif datatype_input == datatype_dict[8]:
                datatype = "Incremento"
                articles = Articles.objects.filter(increase__icontains=article_input)
            else: #datatype_input == datatype_dict[9]:
                datatype = "Precio de venta"
                articles = Articles.objects.filter(sell_price__icontains=article_input)
            
            if not articles:

                answer_negative = "No se encuentra:"

                context={"articles_searched":articles,"article_input":article_input, "articles_any": articles, "answer_negative": answer_negative, "datatype_input": datatype }
                return section_articles_deliver(request,context)
            
            else:

                answer = "Se está buscando:"
        
                context={"articles_searched":articles,"article_input":article_input, "articles_any": articles, "datatype_input": datatype, "answer": answer}
                return section_articles_deliver(request,context)
        
        else:

            answer_negative = "Por favor, completa el campo de búsqueda"
            answer = "Artículos en la Base de datos"
            articles = Articles.objects.all()
            context = {"articles_all":articles, "articles_any": articles, "answer_negative":answer_negative, "answer":answer}
            return section_articles_deliver(request, context)

def section_articles_categories_deliver(request, context: dict): 

    return render(request,"categories.html", context)

def section_articles_categories(request):

    first_time_categories = request.GET['first_time_categories']

    if first_time_categories == '1':

        categories = Categories.objects.all()
        context = {"categories": categories}
        return section_articles_categories_deliver(request, context)
    
    else:

        category_input = request.GET['category_input']
    
        context = {"category_input": category_input}
        return section_articles_categories_deliver(request, context)

def section_articles_crud_deliver(request, context):
    return render(request,template_name="articles_crud.html", context={})

def article_create(request):
    pass #te debe reenviar al formulario html para agregar articulos
    #section_articles_crud_deliver(request)

def article_delete(request):
    pass #te debe eliminar el artículo seleccionado. toma los valores de ese artículo y los busca en la tabla para eliminarlos
    #section_articles_crud_deliver(request)

def article_update(request):
    pass
    #section_articles_crud_deliver(request)

def article_crud_confirm(request):
    pass