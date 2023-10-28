from random import choices
import attr
from django import forms
from orders.models import Order
from articles.models import Article
class OrderForm(forms.ModelForm):
    
    class Meta:
        choices = [('True','Done'),('None','Pending'),('False','Canceled')]
        model = Order
        fields=['customer_id', 'articles_cart', 'details', 'delivery_status']
        widgets = {
            'customer_id': forms.Select(attrs={'class':'select select-bordered w-full'}),
            'articles_cart': forms.SelectMultiple(attrs={'class':'select select-bordered w-full'}),
            'details': forms.Textarea(attrs={'class':'textarea textarea-bordered w-full'}),
            'delivery_status': forms.Select(attrs={'class':'select select-bordered w-full'}, choices=choices)
        }