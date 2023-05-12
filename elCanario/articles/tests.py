from django.test import Client, TestCase
from django.urls import reverse
from .models import *
from django.contrib.auth.models import User
"""class MyTests(TestCase):
    def test_example_view(self):
        client = Client()
        # reverse(nombre de la url) indica que url se utilizará para la petición
        response = client.get(reverse('my_view'), data={'article_name_input': 'hola'})
        self.assertEqual(response.status_code, 200)
        #assertEqual 
        self.assertEqual(response.context['saludo'], 'el artículo está saludando')
        #Este código verifica que la plantilla se haya utilizado en la respuesta de la vista 
        self.assertTemplateUsed(response, 'ejemplo.html')
class MyTests(TestCase):
    def test_example_view(self):
        client = Client()
        response = client.get(reverse('my_view'))
        self.assertEqual(response.status_code, 200)
        #assertContains verifica que exita un valor ?
        self.assertContains(response, 'el artículo está saludando')
        #verifica que saludo no este presente en el contexto
        self.assertNotIn('saludo', response.context)"""
class Test_articles(TestCase):

    def setUp(self):
        # Crea un usuario de prueba
        self.user = User.objects.create_user(username='admin', password='1234')
        #crear artículos para mi base de datos de prueba
        article = Article.objects.create(
            name = 'articlename',
            buy_price = 10,
            increase = 20,
            sell_price = 12
        )
        category = Category.objects.create(
            name = 'categoryname'
        )
        value = Value(
            name = 'valuename',
            category_id = category
        )
        article_value = ArticleValue(
            article_id = article,
            category_id = category,
            value_id = value
        )

        article.save()
        category.save()
        value.save()
        article_value.save()

    def test_articles(self):


        client = Client()
        client.login(username = 'admin', password = '1234')

        response = client.get(reverse('articles'))

        articles = Article.objects.all()

        answer = "Artículos en la Base de datos"
        expected_context = {
            "answer":answer,
            "datatype_input": 'name',
            "datatype": 'Nombre'
        }

        #Al tener un error de comparacion con las QuerySet se hará de la siguiente manera:
        #para las respuestas de contextos que contengan objetos...
        self.assertQuerysetEqual(response.context['articles_any'], articles)
        self.assertDictContainsSubset(expected_context,response.context)
        # determinamos el template que debería utilizar
        self.assertTemplateUsed(response, 'articles.html')
        #determinamos el codigo de respuesta
        self.assertEqual(response.status_code, 200)

    def test_articles_read_datatype(self):

        # 1- determinamos la url-name que se utiliza y los valores que recibirá la función
        client = Client()
        response = client.get(reverse('articles_read_datatype'), data={'datatype_input': 'name'})
        #logeamos
        client.login(username = 'admin', password = '1234')
        # 2- elementos en el contexto:
            #Modelos que utilizamos de la base de datos
        articles = Article.objects.all()
            #contexto específico
        expected_context = {
            "datatype_input": 'name',
            "datatype": "Nombre"
        }
        print(response.context) # declaracion de depuracion
        print("articles_any:", articles)
        
            #Al tener un error de comparacion con las QuerySet se hará de la siguiente manera:
            #para las respuestas de contextos que contengan objetos...
        self.assertQuerysetEqual(response.context['articles_any'], articles)
        self.assertDictContainsSubset(expected_context,response.context)
        # 3- determinamos el template que debería utilizar
        self.assertTemplateUsed(response, 'articles_search_datatype.html')
        # 4- determinamos el codigo de respuesta
        self.assertEqual(response.status_code, 200)


    
    