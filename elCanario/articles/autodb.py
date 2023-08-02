#AUTO GENERATE fields
from .models import Article, Category, Value, ArticleValue
import random


def generate_articles(num):
    names = ["co", "la","fla","men","pri","pro","sul","so","fa","ar","si","lla","fre","ir","gas","dor","mir","cro","no","va","ri","ta"]
    for _ in range(num):
        article = Article(
            name = f"{random.choice(names)}" + f"{random.choice(names)}" + f"{random.choice(names)}",
            buy_price = random.uniform(100, 500),
            increase = random.uniform(0,300),
        )
        article.sell_price = article.buy_price + ((article.buy_price * article.increase) / 100)

        try:
            article.save()
            
        except:
            num -= 1
            pass
    print(f"{num} articles generated correctly!")

def generate_categories_values(num_cat, num_val):
    names = ["Material", "Tipo", "Color", "Forma", "Tamaño", "Peso", "Marca", "Modelo", "Estilo", "Textura", "Sabor", "Olor", "Sonido", "Temperatura", "Dureza", "Flexibilidad", "Transparencia", "Brillo", "Elasticidad", "Resistencia", "Impermeabilidad", "Porosidad", "Adherencia", "Conductividad", "Reflectividad", "Refractividad", "Densidad", "Viscosidad", "Solubilidad","Fragilidad"]
    for _ in range(num_cat):
        category = Category(
            name = random.choice(names)
        )
        try:
            category.save()
        except:
            num_cat -= 1
            pass
        else:
            names = ["Algodón", "Seda", "Lana", "Cuero", "Madera", "Metal", "Plástico", "Vidrio", "Piedra", "Papel", "Zapato", "Camisa", "Pantalón", "Vestido", "Sombrero", "Guante", "Bufanda", "Corbata", "Rojo", "Azul", "Verde", "Amarillo", "Naranja", "Morado", "Negro", "Blanco", "Gris", "Marrón", "Rosa", "Beige","Circular","Cuadrado","Triangular","Rectangular","Hexagonal","Pequeño","Mediano","Grande","Ligero","Pesado","Nike","Adidas","Puma","Reebok","Under Armour","Levis","Calvin Klein","Tommy Hilfiger","Ralph Lauren","Lacoste","Moderno","Clásico","Vintage","Rústico","Urbano","Elegante","Casual","Deportivo","Suave","Áspero","Dulce","Salado","Amargo","Ácido","Picante","Umami","Floral","Cítrico","Herbáceo","Amaderado","Silencioso","Ruidoso","Musical"]
            for _ in range(num_val):

                value = Value(
                    category_id = category,
                    name = random.choice(names)
                )
                try:
                    value.save()
                except:
                    num_val -= 1
                    pass
        print(f"{num_val} values for {category.name} generated correctly!")
    print(f"{num_cat} categories generated correctly!") 

def generate_category_values_for_articles(num):
    values = Value.objects.all()
    articles = Article.objects.all()
    for _ in range(num):
        value_choiced = random.choice(values)
        article_value = ArticleValue(
            category_id = value_choiced.category_id,
            value_id = value_choiced,
            article_id = random.choice(articles)
        )
        
        try:
            article_value.save()
        except:
            num -= 1
            pass
    print(f"{num} relations category values for articles")

def generate(num):
    generate_articles(num*2)
    generate_categories_values(num,round(num/2))
    generate_category_values_for_articles(num*20)

"""for fast use:
    Enter to shell:

        py manage.py shell
    
    In shell use generate functions:
        from articles import autodb
        generate(x)
"""
