# ARTICLES

---

## CREATE

- ArticleCreateView

:::elCanario.articles.views.ArticleCreateView

- articles_create_name_check

:::elCanario.articles.views.articles_create_name_check

- articles_create_calculator

:::elCanario.articles.views.articles_create_calculator

- create_stock_check

:::elCanario.articles.views.create_stock_check

- articles_create_confirm

:::elCanario.articles.views.articles_create_confirm

---

## READ

- ArticleListView

:::elCanario.articles.views.ArticleListView

- ReadDataListView

:::elCanario.articles.views.ReadDataListView

- ReadDatatypeListView

:::elCanario.articles.views.ReadDatatypeListView

---

## UPDATE

> Update uses the same validator functions as CREATE except for the name and to confirm the update of the article.

- ArticleDetailView

:::elCanario.articles.views.ArticleDetailView

- articles_update_name_check

:::elCanario.articles.views.articles_update_name_check

- articles_update_confirm

:::elCanario.articles.views.articles_update_confirm

---

## DELETE

- article_delete

:::elCanario.articles.views.article_delete

---

## Categories - Values

## CREATE - Categories

- articles_category_create
  
:::elCanario.articles.views.articles_category_create

## READ - Categories

- CategoriesView
  
:::elCanario.articles.views.CategoriesView

## UPDATE - Categories

- articles_category_update_name
  
:::elCanario.articles.views.articles_category_update_name

## DELETE - Categories

- articles_category_delete
  
:::elCanario.articles.views.articles_category_delete

## CREATE - Values

- articles_category_value_create
  
:::elCanario.articles.views.articles_category_value_create

## READ - Values

- articles_category_update
  
    > Enables editing of the articles belonging to that category

:::elCanario.articles.views.articles_category_update

- articles_value_update

    > Enables editing of the value name
  
:::elCanario.articles.views.articles_value_update

## UPDATE - Values

- articles_value_update_name
  
:::elCanario.articles.views.articles_value_update_name

## DELETE - Values

- articles_value_delete
  
:::elCanario.articles.views.articles_value_delete
