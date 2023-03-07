from django.shortcuts import render
from articles.models import Articles
from django.http import HttpResponse
# Create your views here.

def search_article(request):

    article_input = request.GET['article_input']

    if article_input:

        articles = Articles.objects.filter(article_name__icontains=article_input)
        return render(request,"articles.html",context={"articles":articles,"query_search":article_input, "answer_search": "No se encuentra ningun artículo para el nombre buscado:"})
    
    else:
        
        return section_articles(request)
    
def section_orders(request):
    return render(request, template_name="orders.html",context={})
def section_customers(request):
    return render(request, template_name="customers.html",context={})
def section_articles(request):
    articles_all = Articles.objects.all()
    return render(request,"articles.html", context={"articles_all":articles_all,"answer_all":"Aún no hay articulos en la base de datos"})

    


