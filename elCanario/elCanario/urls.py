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
from customers import views as customers_views
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
    path('articles', articles_views.articles, name="articles"), #va a articles section
    path('articles_create', articles_views.articles_create, name="articles_create"),
    path('articles_read_datatype', articles_views.articles_read_datatype, name="articles_read_datatype"), #vuelve a articles section
    path('articles_read_data', articles_views.articles_read_data, name="articles_read_data"), #vuelve a articles section
    path('articles_update/<int:id>', articles_views.article_update, name="article_update"),
    path('articles_delete/<int:id>', articles_views.article_delete, name="articles_delete"), #vuelve a articles section
    path('articles/categories', articles_views.articles_categories, name="categories"),

    #CUSTOMERS
    path('customers', customers_views.customers, name="customers"),
    path('customers_create', customers_views.customers_create, name="customers_create"),
    path('customers_read_datatype', customers_views.customers_read_datatype, name="customers_read_datatype"),
    path('customers_read_data', customers_views.customers_read_data, name="customers_read_data"),
    # path('customers_update/<int:id>', articles_views.customers_read_data_update, name="customers_update"),
    # path('customers_delete/<int:id>', articles_views.customers_read_data_delete, name="customers_delete"),
]
htmx_urlpatterns = [
#     #ARTICLES SETCIONS
#       ##ARTICLUES READ FUNCTIONS

        ##ARTICLES CREATE FUNCTIONS
    path('article_create_name_check',articles_views.articles_create_name_check, name="name_check"),
    path('create_sell_price_calculator', articles_views.articles_create_calculator, name="calculator"),
    path('articles_create_confirm', articles_views.articles_create_confirm, name="articles_create_confirm"),
        ##ARTICLES UPDATE FUNCTIONS
    path('article_update_name_check/<int:id>', articles_views.articles_update_name_check, name="name_update_check"),
    path('articles_update_confirm/<int:id>', articles_views.articles_update_confirm, name="articles_update_confirm"),

#         #ARTICLES CATEGORIES
    path('articles_categories_create/<str:art_id>', articles_views.articles_category_create, name="category_create"),
    path('articles_categories_create', articles_views.articles_category_create, name="category_create"),
    path('articles_categories_update/<str:external_link>/<int:cat_id>/<str:art_id>', articles_views.articles_category_update, name="category_update"),
    path('articles_categories_update/<str:external_link>/<int:cat_id>', articles_views.articles_category_update, name="category_update"),
    path('articles_categories_update_name/<int:cat_id>/<str:art_id>', articles_views.articles_category_update_name, name="category_update_name"),
    path('articles_categories_update_name/<int:cat_id>', articles_views.articles_category_update_name, name="category_update_name"),
    path('articles_categories_delete/<int:cat_id>/<str:art_id>', articles_views.articles_category_delete, name="category_delete"),
    path('articles_categories_delete/<int:cat_id>', articles_views.articles_category_delete, name="category_delete"),
    path('articles_categories_values_create/<int:cat_id>/<str:art_id>', articles_views.articles_category_value_create, name="value_create"),
    path('articles_categories_values_create/<int:cat_id>', articles_views.articles_category_value_create, name="value_create"),
    path('articles_categories_values_update/<int:cat_id>/<int:val_id>/<str:art_id>', articles_views.articles_value_update, name="value_update"),
    path('articles_categories_values_update/<int:cat_id>/<int:val_id>', articles_views.articles_value_update, name="value_update"),
    path('articles_categories_values_update/name/<int:val_id>/<str:art_id>', articles_views.articles_value_update_name, name="value_update_name"),
    path('articles_categories_values_update/name/<int:val_id>', articles_views.articles_value_update_name, name="value_update_name"),
    path('articles_categories_values_delete/<int:cat_id>/<int:val_id>/<str:art_id>', articles_views.articles_value_delete, name="value_delete"),
    path('articles_categories_values_delete/<int:cat_id>/<int:val_id>', articles_views.articles_value_delete, name="value_delete"),

]
urlpatterns += htmx_urlpatterns

if settings.DEBUG:
    
    from django.conf.urls.static import static
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)