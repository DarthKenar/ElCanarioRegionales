from random import choices
import attr
from django import forms
from orders.models import Order
from articles.models import Article
class OrderForm(forms.ModelForm):
    
    class Meta:
        trigger = {'hx-trigger':'blur'}
        choices = [('True','Done'),('None','Pending'),('False','Canceled')]
        model = Order
        fields=['customer_id', 'articles_cart', 'details', 'delivery_status']
        widgets = {
            'customer_id': forms.Select(attrs=trigger),
            'articles_cart': forms.SelectMultiple(attrs=trigger),
            'details': forms.Textarea(attrs=trigger),
            'delivery_status': forms.Select(attrs=trigger, choices=choices)
        }