# Welcome to El Canario Regionales

![El Canario Regionales Logo](images/logo-header.png)

## Description

[@elcanario.regionales](https://www.instagram.com/elcanario.regionales/)

## Features

- Create, edit, delete _customers_.
- Creates, edits, deletes _items_ for articles
  - Creates, edits or deletes _categories_ for articles
    - Creates, edits or deletes _values_ related to a specific category (to relate them to a specific article)
- Create, edit, delete _orders_.
- Automatic creation of log of actions displayed on the main panel (desktop)
- Full authentication system
  - Login (or register) with Google account
  - Registration
  - Login with Google account
  - Password recovery
  - Email confirmation (not mandatory for practical purposes)
  - Dual authentication system (2FA) (not mandatory for practical purposes)
  - and much more...
- Filtering of Cards (objects [Customers, Orders, Items]) based on any of their attributes (Implemented HTMX dynamic page)
- Install the application on your cell phone (Progressive web application)

## Project layout

``` bash

app_name/
    template/app_name
        htmx
            *.html
        partials
            *.html
        *.html
DataBase
manage.py
```

## Models Relationships

``` mermaid
erDiagram 
    Article one or zero to many ArticleValue : characteristics_id
    Article |o--|| ArticlePromotion : in
    Article |o--|| ArticleOrder : in
    ArticleValue |o--|| Value : get
    ArticleValue |o--|| Category : get
    Value |o--|| Category : get
    ArticlePromotion |o--|| Promotion : get
    ArticleOrder |o--|| Order : get
    Order |o--|| Customer : places
    Article {
        id BigAutoField
        image Imagefield
        name CharField
        buy_price DecimalField
        increase DecimalField
        sell_price DecimalField
        stock PositiveSmallIntergerField
    }
    ArticleValue {
        id BigAutoField
        article_id ForeingKey
        category_id ForeingKey
        value_id ForeingKey
    }
    ArticlePromotion {
        id BigAutoField
        article_id ForeingKey
        promotion_id ForeingKey
    }
    ArticleOrder {
        id BigAutoField
        article_id ForeingKey
        order_id ForeingKey
    }
    Value {
        id BigAutoField
        name CharField
        category_id ForeingKey
    }
    Category {
        id BigAutoField
        name CharField
    }
    Promotion {
        id BigAutoField
        name CharField
        discount DecimalField
        remainder SmallIntergerField
        sell_price DecimalField
    }
    Order {
        id BigAutoField
        customer_id ForeingKey
        article_quantity PositiveSmallIntergerField
        creation_date DateTimeField
        delivery_status BooleanDield
        details TextField
        total_pay DecimalField
        updated_date DateTimeField
    }
    Customer {
        id BigAutoField
        address CharField
        email EmailField
        name CharField
        phone_number CharField
    }
```

---

## DEPENDENCIES

| Package | Description | Link |
| ----------- | ---|---|
| "django>=4.2.6" | Web framekork | [Django](https://www.djangoproject.com/) |
| "django-allauth>=0.58.1" | Social Authentication |[django-allauth](https://github.com/pennersr/django-allauth)|
| "django-pwa>=1.1.0" | Aplicación Web Progresiva | [django-pwa](https://github.com/silviolleite/django-pwa) |
| "django-widget-tweaks>=1.5.0" | Form Render | [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks) |
| "slippers>=0.6.2" |Components whit template tags| [slippers](https://github.com/mixxorz/slippers) |
| "Pillow>=10.1.0" ||[Pillow](https://github.com/python-pillow/Pillow)|
| "pytz>=2023.3.post1" ||[pytz](https://github.com/stub42/pytz)|

### Tools

- [TailWinds](https://tailwindcss.com/)
- [DaisyUI](https://daisyui.com/)
- [Feathericons](https://feathericons.com/)
- [HTMX](https://htmx.org/)

## PREVIEW

### RESPONSIVE DESIGN

![RESPONSIVE DESIGN](images/responsive_design.png)

### CHANGE LANGUAGE

![CHANGE LANGUAGE](images/switch-lenguage.gif)

### CHANGE THEME

![CHANGE THEME](images/switch-theme.gif)
