from django.db import models

# Create your models here.
class DollarGraph(models.Model):
    
    price = models.FloatField() #it is likely that django will need to be upgraded to store larger numbers, the price of the argentine peso may surprise us.
    date = models.DateField(auto_now_add=True)

    class Meta:

        verbose_name = "Dollar price"
        verbose_name_plural = "Dollar prices"
        ordering = ['id']