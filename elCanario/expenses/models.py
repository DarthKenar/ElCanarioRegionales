from django.db import models

# Create your models here.




class Expense(models.Model):

    name = models.CharField(verbose_name="Name", max_length=32)
    description = models.TextField(verbose_name="Description", max_length=128, blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(verbose_name="Quantity", default=1)
    total_cost = models.DecimalField(verbose_name="Price", max_digits=10, decimal_places=2)

    class Meta:

        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ['total_cost']
    
    def __str__(self) -> str:

        return f"{self.name},{self.description},{self.quantity},{self.total_cost}"