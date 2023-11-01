from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
# Create your models here.
def allowed_emails(value):
    emails = [
        "@gmail.com",
        "@hotmail.com",
        "@outlook.com",
        "@outlook.com.es",
        "@yahoo.com.ar"
    ]
    if value[value.find('@')::] in emails:
        print(value)
        print(value[value.find('@')::])
        return value
    else:
        raise ValidationError(_("The e-mail entered is not in the list of allowed e-mails."))
        
def min_len(value):
    if len(value) >= 7:
        return value
    else:
        raise ValidationError(_("The Dni must not be less than 7 digits long."))

class Customer(models.Model):
    name = models.CharField(max_length=100)
    dni = models.CharField(null=True, blank=True, unique=True, max_length=8, validators=[RegexValidator(r'^\d{1,10}$')])
    phone_number = models.CharField(null=True, blank=True, unique=True, max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True, unique=True, validators=[allowed_emails])
    total_purchased = models.DecimalField(max_digits=10, decimal_places=2, editable=False, blank=True, null=True, default=0)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['name']
    
    def __str__(self) -> str:
        return f"{self.name},\n{self.phone_number}"
    
