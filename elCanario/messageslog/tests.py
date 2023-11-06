from django.test import TestCase
from articles.models import Article, Category, Value
from customers.models import Customer
from orders.models import Order
from messageslog.models import MessageLog

class TestCase(TestCase):
    def setUp(self):
        Article.objects.create(name="Mesa",buy_price=20,increase=10,sell_price=22,stock=2)
    def test_messageslog_articles_create(self):
        exists = MessageLog.objects.all()
        self.assertIsNotNone(exists)