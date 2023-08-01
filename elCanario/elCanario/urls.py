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
from django.urls import path, include

from authentication import views as auth_views
from customers import views as customers_views
from orders import views as orders_views
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),

    #LOGIN SECTION & HOME
    path('', auth_views.login_view, name="login"),
    path('login_search/', auth_views.search_user, name="login_search"),
    path('home', auth_views.home, name="home"),

    # ORDERS SECTION
    path('orders', orders_views.orders, name="orders"),

    ## ARTICLES SECTIONS
    path('articles', include('articles.urls')), #va a articles section


    #CUSTOMERS
    path('customers', customers_views.customers, name="customers"),
    path('customers_create', customers_views.customers_create, name="customers_create"),
    path('customers_read_datatype', customers_views.customers_read_datatype, name="customers_read_datatype"),
    path('customers_read_data', customers_views.customers_read_data, name="customers_read_data"),
    # path('customers_update/<int:id>', articles_views.customers_read_data_update, name="customers_update"),
    # path('customers_delete/<int:id>', articles_views.customers_read_data_delete, name="customers_delete"),
]

if settings.DEBUG:
    
    from django.conf.urls.static import static
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)