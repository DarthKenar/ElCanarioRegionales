from django.db import models
from articles import models as articles_models
from customers import models as customers_models
# Create your models here.
class Order(models.Model):

    customer_id = models.ForeignKey(customers_models.Customer,verbose_name="Customer", on_delete=models.CASCADE)
    article_id = models.ManyToManyField(articles_models.Article, verbose_name="Articles",related_name="articles_cart", through="ArticleOrder")
    article_quantity = models.PositiveSmallIntegerField(verbose_name="Articles Quantity", editable=False, blank=True, null=True)
    total_pay = models.DecimalField(verbose_name="Total pay", max_digits=10, decimal_places=2, editable=False, blank=True, null=True)
    details = models.TextField(verbose_name="Details", blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation date", editable=False, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True,verbose_name="Date last modified", editable=False, blank=True, null=True)
    delivery_status = models.BooleanField(verbose_name="Delivery status", default=False, blank=True, null=True)

    class Meta:

        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['customer_id',]
    
    def __str__(self) -> str:

        return f"Customer: {self.customer_id.name}, phone: {self.customer_id.phone_number}, total: {self.total_pay}, status: {self.delivery_status}"


class ArticleOrder(models.Model):
    article_id = models.ForeignKey(articles_models.Article,on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)