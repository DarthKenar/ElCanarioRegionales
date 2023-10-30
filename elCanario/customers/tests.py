from django.test import TestCase
from customers.models import Customer
from messageslog.models import MessageLog
# Create your tests here.
# class MessageLogTestCase(TestCase):
#     def setUp(self):
#         Customer.objects.create(name="Federico",dni="12345678",phone_number="1234567890",address="Av. San Martín 1234", email="federico_vega@hotmail.com",total_purchased=500)
    
#     def test_email_allowed(self):
#         quantity = MessageLog.objects.all().count()
#         self.assertEqual(quantity, 1)