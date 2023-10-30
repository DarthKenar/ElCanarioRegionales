from django.contrib import admin
from django.urls import path, include
from articles import views as articles_views
from _core.views import IndexView
urlpatterns = [
    #https://docs.djangoproject.com/en/dev/topics/i18n/translation/#the-set-language-redirect-view
    path("i18n/", include("django.conf.urls.i18n")),

    #settings module
    path('', include('_core.urls')),
    path('', include('settings.urls')),

    #https://docs.allauth.org/en/latest/
    path('accounts/', include('allauth.urls')),
 
    #https://pypi.org/project/django-pwa/
    #https://github.com/silviolleite/django-pwa
    path('', include('pwa.urls')),

    # ADMIN
    path('admin/', admin.site.urls),

    # ORDERS SECTIONS
    path('orders/', include('orders.urls')),

    # ARTICLES SECTIONS
    path('articles/', include('articles.urls')),

    #CUSTOMERS SECTIONS
    path('customers/', include('customers.urls')),

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
    path('articles_categories_update/<str:external_link>/<int:cat_id>', articles_views.articles_category_update, name="category_update"),
    path('articles_categories_update/<str:external_link>/<int:cat_id>/<str:art_id>', articles_views.articles_category_update, name="category_update"),
    path('articles_categories_update_name/<int:cat_id>', articles_views.articles_category_update_name, name="category_update_name"),
    path('articles_categories_update_name/<int:cat_id>/<str:art_id>', articles_views.articles_category_update_name, name="category_update_name"),
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

from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    from django.conf.urls import include
    urlpatterns += [
        path(r'translate/', include('rosetta.urls')),
    ]