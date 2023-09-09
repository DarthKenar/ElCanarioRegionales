from django.db import models
from django.core.validators import RegexValidator
# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    dni = models.CharField(null=True, blank=True, unique=True, max_length=8, validators=[RegexValidator(r'^\d{1,10}$')])
    phone_number = models.CharField(null=True, blank=True, unique=True, max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True, unique=True)
    total_purchased = models.DecimalField(max_digits=10, decimal_places=2, editable=False, blank=True, null=True, default=0)

    class Meta:

        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['name']
    
    def __str__(self) -> str:

        return f"{self.name},\n{self.phone_number}"