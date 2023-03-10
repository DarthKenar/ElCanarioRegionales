from django.shortcuts import render
from articles.models import Articles, Categories
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

    first_time_articles = request.GET['first_time_articles'] #no se porque tira error
    #first_time_articles = '1'
    if first_time_articles == '1':

        answer = "Artículos en la Base de datos"
        articles = Articles.objects.all()
        context = {"articles_all":articles, "articles_any": articles, "answer":answer}
        return section_articles_deliver(request, context)
    
    else:

        datatype = {
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

            if datatype_input == datatype[1]:
                data_type = "ID"
                articles = Articles.objects.filter(id__icontains=article_input)
            elif datatype_input == datatype[2]:
                data_type = "Nombre"
                articles = Articles.objects.filter(article_name__icontains=article_input)
            elif datatype_input == datatype[3]:
                data_type = "Categoría"
                articles = Categories.objects.filter(category_id__icontains=article_input)
            elif datatype_input == datatype[4]:
                data_type = "Color"
                articles = Articles.objects.filter(color_id__icontains=article_input)
            elif datatype_input == datatype[5]:
                data_type = "Material"
                articles = Articles.objects.filter(material_id__icontains=article_input)
            elif datatype_input == datatype[6]:
                data_type = "Talle/Tamaño"
                articles = Articles.objects.filter(size_id__icontains=article_input)
            elif datatype_input == datatype[7]:
                data_type = "Precio de compra"
                articles = Articles.objects.filter(buy_price__icontains=article_input)
            elif datatype_input == datatype[8]:
                data_type = "Incremento"
                articles = Articles.objects.filter(increase__icontains=article_input)
            else: #datatype_input == datatype[9]:
                data_type = "Precio de venta"
                articles = Articles.objects.filter(sell_price__icontains=article_input)
            
            if not articles:

                answer_negative = "No se encuentra:"

                context={"articles_searched":articles,"article_input":article_input, "articles_any": articles, "answer_negative": answer_negative, "datatype_input": datatype_input }
                return section_articles_deliver(request,context)
            
            else:

                answer = "Se está buscando:"
        
                context={"articles_searched":articles,"article_input":article_input, "articles_any": articles, "datatype_input": datatype_input, "answer": answer}
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





