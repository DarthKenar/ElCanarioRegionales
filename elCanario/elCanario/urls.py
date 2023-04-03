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
    path('', auth_views.login_view, name="login"),
    path('login_search/', auth_views.search_user, name="login_search"),
    path('home', auth_views.home, name="home"),

    # ORDERS SECTION
    path('orders', articles_views.orders, name="orders"),

    ## ARTICLES SECTIONS
    path('articles', articles_views.articles, name="articles"),

    path('articles_create', articles_views.articles_create, name="articles_create"),
    path('articles_read', articles_views.articles_read, name="articles_read"),
    path('articles_update/<int:id>', articles_views.articles_update, name="articles_update"),
    path('articles_delete/<int:id>', articles_views.articles_delete, name="articles_delete"),

    path('articlesCategories', articles_views.articles_categories, name="categories"),
    path('articlesColors', articles_views.articles_colors, name="colors"),
    path('articlesMaterials', articles_views.articles_materials, name="materials"),
    path('articlesSizes', articles_views.articles_sizes, name="sizes"),

    #CUSTOMERS
    path('customers', articles_views.customers, name="customers"),
    
]

htmx_urlpatterns = [
    #ARTICLES SETCIONS
        ##ARTICLUES READ FUNCTIONS
    path('articles_read_id', articles_views.articles_read_id, name="articles_read_id"),
    path('articles_read_name', articles_views.articles_read_name, name="articles_read_name"),
    path('articles_read_category', articles_views.articles_read_category, name="articles_read_category"),
    path('articles_read_color', articles_views.articles_read_color, name="articles_read_color"),
    path('articles_read_material', articles_views.articles_read_material, name="articles_read_material"),
    path('articles_read_size', articles_views.articles_read_size, name="articles_read_size"),
    path('articles_read_buy_price', articles_views.articles_read_buy_price, name="articles_read_buy_price"),
    path('articles_read_increase', articles_views.articles_read_increase, name="articles_read_increase"),
    path('articles_read_sell_price', articles_views.articles_read_sell_price, name="articles_read_sell_price"),

        ##ARTICLES CREATE FUNCTIONS
    path('article_create_name_check',articles_views.articles_create_name_check, name="name_check"),
    path('articles_create_category_check', articles_views.articles_create_category_check, name="category_check"),
    path('create_sell_price_calculator', articles_views.articles_create_calculator, name="calculator"),
    path('articles_create_confirm', articles_views.articles_create_confirm, name="articles_create_confirm"),

        ##ARTICLES UPDATE FUNCTIONS
    path('article_update_name_check/<int:id>',articles_views.articles_update_name_check, name="update_name_check"),
    path('articles_update_category_check/<int:id>', articles_views.articles_update_category_check, name="update_category_check"),
    path('update_sell_price_calculator/<int:id>', articles_views.articles_update_calculator, name="update_calculator"),
    path('articles_update_confirm/<int:id>', articles_views.articles_update_confirm, name="articles_update_confirm"),

        #ARTICLES CATEGORIES
    path('articles/categories/save', articles_views.articles_categories_save, name="category_save"),
    path('articles/categories/update/<int:id>', articles_views.articles_categories_update, name="category_update"),
    path('articles/categories/delete/<int:id>', articles_views.articles_categories_delete, name="category_delete"),

        #ARTICLES COLORS
    path('articles/colors/save', articles_views.articles_colors_save, name="color_save"),
    path('articles/colors/update/<int:id>', articles_views.articles_colors_update, name="color_update"),
    path('articles/colors/delete/<int:id>', articles_views.articles_colors_delete, name="color_delete"),

        #ARTICLES MATERIALS
    path('articles/materials/save', articles_views.articles_materials_save, name="material_save"),
    path('articles/materials/update/<int:id>', articles_views.articles_materials_update, name="material_update"),
    path('articles/materials/delete/<int:id>', articles_views.articles_materials_delete, name="material_delete"),

        #ARTICLES SIZES
    path('articles/sizes/save', articles_views.articles_sizes_save, name="size_save"),
    path('articles/sizes/update/<int:id>', articles_views.articles_sizes_update, name="size_update"),
    path('articles/sizes/delete/<int:id>', articles_views.articles_sizes_delete, name="size_delete"),
]
urlpatterns += htmx_urlpatterns


#STATIC AND IMAGES
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.IMG_URL, document_root = settings.IMG_ROOT)