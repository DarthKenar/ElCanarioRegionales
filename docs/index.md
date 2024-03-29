# Welcome to El Canario Regionales

![El Canario Regionales Logo](images/logo-header.png)

## Description

Originally the web application El Canario Regionales was created for the management of a small business of regional articles from Argentina ([@elcanario.regionales](https://www.instagram.com/elcanario.regionales/)), although its use can be general for any CRM business.
Given its nature and scalability it would be a matter of replacing logos, fonts and some other small things.
Using DaisyUI this becomes very simple.

## Features

- Create, edit, delete _customers_.

- Creates, edits, deletes _articles_.
  - Creates, edits or deletes _categories_ for articles
  - Creates, edits or deletes _values_ related to a specific category (to relate them to a specific article)

- Create, edit, delete _orders_.

- Automatic creation of log of actions displayed on the main panel (desktop)

- Full authentication system
  - Log In (or Sign Up) with Google account
  - Log In - Sign Up Standard Mode
  - Password recovery
  - Email confirmation (disabled for practical purposes)
  - Dual authentication system (disabled for practical purposes)
  - and more...

- Filtering of Cards (objects [Customers, Orders, Articles]) based on any of their attributes (Implemented HTMX dynamic page)

- Install the application on your cell phone (Progressive web application)

- Change lenguage for your account

- Change theme for your account

- All actions taken will be saved and displayed on dashboard.

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

## Main Models Relationships

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

## Dependencies

| Package | Description | Link |
| ----------- | ---|---|
| "django>=4.2.6" | Web framekork | [Django](https://www.djangoproject.com/) |
| "django-allauth>=0.58.1" | Social Authentication |[django-allauth](https://github.com/pennersr/django-allauth)|
| "django-pwa>=1.1.0" | Progressive Web Aplication | [django-pwa](https://github.com/silviolleite/django-pwa) |
| "django-widget-tweaks>=1.5.0" | Form Render | [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks) |
| "slippers>=0.6.2" |Components whit template tags| [slippers](https://github.com/mixxorz/slippers) |
| "Pillow>=10.1.0" |Images|[Pillow](https://github.com/python-pillow/Pillow)|
| "pytz>=2023.3.post1" |Time Zone|[pytz](https://github.com/stub42/pytz)|

### Notes

For django-allauth I have disabled two-factor authentication, email confirmation (verification) and some other features for practical purposes, so that anyone who wants to log in and test the application would find it easier.

### Tools

- [TailWinds](https://tailwindcss.com/)
- [DaisyUI](https://daisyui.com/)
- [Feathericons](https://feathericons.com/)
- [HTMX](https://htmx.org/)

## Preview

### Responsive Design

![RESPONSIVE DESIGN](images/responsive_design.png)

### Change lenguage

![CHANGE LANGUAGE](images/switch-lenguage.gif)

### Change theme

![CHANGE THEME](images/switch-theme.gif)
