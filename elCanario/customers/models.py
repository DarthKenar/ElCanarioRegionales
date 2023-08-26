from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    total_purchased = models.DecimalField(max_digits=10, decimal_places=2, editable=False, blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:

        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['name']
    
    def __str__(self) -> str:

        return f"{self.name}, {self.phone_number}"