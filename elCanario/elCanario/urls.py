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


urlpatterns = [
    path('admin/', admin.site.urls),

    #LOGIN SECTION & HOME
    path('', auth_views.login, name="login"),
    path('login/buscar/', auth_views.search_user, name="login_search"),
    path('home', auth_views.home, name="home"),

    # ORDERS SECTION
    path('orders', articles_views.orders, name="orders"),

    ## ARTICLES SECTIONS
    path('articles', articles_views.articles, name="articles"),
    
    path('articlesCategories', articles_views.articles_categories, name="categories"),
    path('articlesColors', articles_views.articles_colors, name="colors"),
    path('articlesMaterials', articles_views.articles_materials, name="materials"),
    path('articlesSizes', articles_views.articles_sizes, name="sizes"),

    #CUSTOMERS
    path('customers', articles_views.customers, name="customers"),

]

htmx_urlpatterns = [
    path('sell_price_calculator', articles_views.sell_price_calculator, name="calculator"),
    
    path('articles/categories/save', articles_views.articles_categories_save, name="category_save"),

    #revisar bien estas urls -  pasarlas a HTMX
    path('articles_create', articles_views.articles_create, name="articles_create"),
    path('articles_create/confirm', articles_views.articles_create_confirm, name="articles_create_confirm"),

    path('articles_read', articles_views.articles_read, name="articles_read"),
    path('articles_update', articles_views.articles_update, name="articles_update"),
    path('articles_delete', articles_views.articles_delete, name="articles_delete"),
]
urlpatterns += htmx_urlpatterns


#STATIC AND IMAGES
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.IMG_URL, document_root = settings.IMG_ROOT)