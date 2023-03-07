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

#Para archivos estaticos durante el desarrollo, no deben estar en produccion
#For static files during development, they must not be in production.
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    #Este es el login (LOGRADO), deberia usar el admin de django
    #This is the login (DONE), I should use django admin.
    path('', auth_views.login), 
    path('login/buscar/', auth_views.search_user),
    
    #Estas son las vistas que deriban a cada una de las secciones de control (Pedidos, Artículos, Clientes)
    #These are the views that lead to each of the control sections (Orders, Articles, Customers).
    path('orders', articles_views.section_orders),

    path('articles', articles_views.section_articles),
    path('articles/search/', articles_views.search_article),

    path('customers', articles_views.section_customers),

]