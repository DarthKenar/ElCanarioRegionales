from django.urls import path
from articles.views import ArticleListView, ArticleDetailView, Read_datatypeListView, Read_dataListView

articles_urlpatterns = ([

    path('',ArticleListView.as_view(),name='articles'),
    
    #       ARTICLUES READ FUNCTIONS

    # path('create', articles_views.articles_create, name="create"),
    path('read_datatype', Read_datatypeListView.as_view(), name="read_datatype"),
    path('read_data', Read_dataListView.as_view(), name="read_data"),
    path('update/<int:pk>', ArticleDetailView.as_view(), name="update"),
    # path('delete/<int:id>', articles_views.article_delete, name="delete"),
    # path('categories', articles_views.articles_categories, name="categories"),

    #       ARTICLES CREATE FUNCTIONS

    # path('create_name_check',articles_views.articles_create_name_check, name="name_check"),
    # path('create_sell_price_calculator', articles_views.articles_create_calculator, name="calculator"),
    # path('create_confirm', articles_views.articles_create_confirm, name="create_confirm"),

    #       ARTICLES UPDATE FUNCTIONS

    # path('update_name_check/<int:pk>', articles_views.articles_update_name_check, name="name_update_check"),
    # path('update_confirm/<int:id>', articles_views.articles_update_confirm, name="update_confirm"),

    #       ARTICLES CATEGORIES

    # path('categories_create/<str:art_id>', articles_views.articles_category_create, name="category_create"),
    # path('categories_create', articles_views.articles_category_create, name="category_create"),
    # path('categories_update/<str:external_link>/<int:cat_id>/<str:art_id>', articles_views.articles_category_update, name="category_update"),
    # path('categories_update/<str:external_link>/<int:cat_id>', articles_views.articles_category_update, name="category_update"),
    # path('categories_update_name/<int:cat_id>/<str:art_id>', articles_views.articles_category_update_name, name="category_update_name"),
    # path('categories_update_name/<int:cat_id>', articles_views.articles_category_update_name, name="category_update_name"),
    # path('categories_delete/<int:cat_id>/<str:art_id>', articles_views.articles_category_delete, name="category_delete"),
    # path('categories_delete/<int:cat_id>', articles_views.articles_category_delete, name="category_delete"),
    # path('categories_values_create/<int:cat_id>/<str:art_id>', articles_views.articles_category_value_create, name="value_create"),
    # path('categories_values_create/<int:cat_id>', articles_views.articles_category_value_create, name="value_create"),
    # path('categories_values_update/<int:cat_id>/<int:val_id>/<str:art_id>', articles_views.articles_value_update, name="value_update"),
    # path('categories_values_update/<int:cat_id>/<int:val_id>', articles_views.articles_value_update, name="value_update"),
    # path('categories_values_update/name/<int:val_id>/<str:art_id>', articles_views.articles_value_update_name, name="value_update_name"),
    # path('categories_values_update/name/<int:val_id>', articles_views.articles_value_update_name, name="value_update_name"),
    # path('categories_values_delete/<int:cat_id>/<int:val_id>/<str:art_id>', articles_views.articles_value_delete, name="value_delete"),
    # path('categories_values_delete/<int:cat_id>/<int:val_id>', articles_views.articles_value_delete, name="value_delete")
], 'articles')