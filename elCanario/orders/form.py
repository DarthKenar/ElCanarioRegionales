from random import choices
from django import forms
from orders.models import Order
from articles.models import Article
from django.utils.translation import gettext_lazy as _
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
        labels = {
            'customer_id': _('Customer'),
            'articles_cart': _('Articles'),
            'details': _('Details'),
            'delivery_status': _('Status'),
        }

    def clean(self):
        cleaned_data = super().clean()
        customer_id = cleaned_data.get('customer_id')
        delivery_status = cleaned_data.get('delivery_status')

        if delivery_status == None:
            existing_orders = Order.objects.filter(customer_id=customer_id)
            if existing_orders.exists():
                self.add_error('customer_id',f"A pending order already exists for the customer {customer_id.name}")

        return cleaned_data