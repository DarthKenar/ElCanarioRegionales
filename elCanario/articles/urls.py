from django.urls import path
# from articles.views import ArticlesListView
from articles import views as articles_views
urlpatterns = [

    path('',articles_views.ArticlesListView.as_view(),name='articles'),
    
    #       ARTICLUES READ FUNCTIONS

    path('articles_create', articles_views.articles_create, name="articles_create"),
    path('articles_read_datatype', articles_views.articles_read_datatype, name="articles_read_datatype"), #vuelve a articles section
    path('articles_read_data', articles_views.articles_read_data, name="articles_read_data"), #vuelve a articles section
    path('articles_update/<int:id>', articles_views.article_update, name="article_update"),
    path('articles_delete/<int:id>', articles_views.article_delete, name="articles_delete"), #vuelve a articles section
    path('articles/categories', articles_views.articles_categories, name="categories"),

    #       ARTICLES CREATE FUNCTIONS

    path('article_create_name_check',articles_views.articles_create_name_check, name="name_check"),
    path('create_sell_price_calculator', articles_views.articles_create_calculator, name="calculator"),
    path('articles_create_confirm', articles_views.articles_create_confirm, name="articles_create_confirm"),

    #       ARTICLES UPDATE FUNCTIONS

    path('article_update_name_check/<int:id>', articles_views.articles_update_name_check, name="name_update_check"),
    path('articles_update_confirm/<int:id>', articles_views.articles_update_confirm, name="articles_update_confirm"),

    #       ARTICLES CATEGORIES

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
    path('articles_categories_values_delete/<int:cat_id>/<int:val_id>', articles_views.articles_value_delete, name="value_delete")
]