"""elCanario URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views 
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from articles import views as articles_views
from authentication import views as auth_views
from django.conf import settings
#Para archivos estaticos durante el desarrollo, no deben estar en produccion
#For static files during development, they must not be in production.
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    #Este es el login (LOGRADO), deberia usar el admin de django
    #This is the login (DONE), I should use django admin.
    path('', auth_views.login, name="home"), 
    path('login/buscar/', auth_views.search_user),
    
    #Estas son las vistas que deriban a cada una de las secciones de control (Pedidos, Artículos, Clientes)
    #These are the views that lead to each of the control sections (Orders, Articles, Customers).
    path('orders', articles_views.orders_all, name="orders_all"),

    path('articles', articles_views.articles_all, name="articles_all"),
    path('articles_create', articles_views.articles_create, name="articles_create"),
    path('articles_read', articles_views.articles_read, name="articles_read"),
    path('articles_update', articles_views.articles_update, name="articles_update"),
    path('articles_delete', articles_views.articles_delete, name="articles_delete"),

    path('articles/categories', articles_views.articles_categories_all, name="categories_all"),

    path('customers', articles_views.customers_all, name="customers_all"),

]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
