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
        
        articles = Articles.objects.all()
        context={"articles_all":articles,"articles_any": articles, "answer_negative":"Aún no hay articulos en la base de datos"}
        return section_articles_deliver(request, context)
    
    else:
            # datatype = {
            #     0: "selection_empty",
            #     1: "id",
            #     2: "article_name",
            #     3: "category_id",
            #     4: "color_id",
            #     5: "material_id",
            #     6: "size_id",
            #     7: "buy_price",
            #     8: "increase",
            #     9: "sell_price"
            # }

        datatype_input = request.GET['datatype_input']
        article_input = request.GET['article_input']
        
        if article_input:

            articles = Articles.objects.filter(article_name__icontains=article_input)
            context={"articles_searched":articles,"query_search":article_input, "articles_any": articles, "answer": "No se encuentra ningun artículo para el nombre buscado:"}
            return section_articles_deliver(request,context)
        
        else:

            articles = Articles.objects.all()
            context = {"articles_all":articles, "articles_any": articles, "answer":"Por favor, completa el campo de búsqueda"}
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





