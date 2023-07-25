from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

class Value(models.Model):
    name = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Category: {self.category_id.name}: Value: {self.name}'
    
    class Meta:
        unique_together = ('name', 'category_id')
        verbose_name = 'Value'
        verbose_name_plural = 'Values'
        ordering = ['name']

class Article(models.Model):
    name = models.CharField(verbose_name="Name",max_length=100, unique=True)
    characteristics_id = models.ManyToManyField(Value,related_name='characteristics_id', blank=True, through='ArticleValue')
    buy_price = models.DecimalField(verbose_name="Buy price", max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    increase = models.DecimalField(verbose_name="Increment", max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    sell_price = models.DecimalField(verbose_name="Sell price", max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])


    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['name']

class ArticleValue(models.Model):
    article_id = models.ForeignKey(Article,on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    value_id = models.ForeignKey(Value,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('article_id', 'category_id')
        verbose_name = "Values and articles Categories"
        verbose_name_plural = "Values and articles Categories"

    def clean(self) -> None:

        if self.category_id != self.value_id.category_id:
            raise ValidationError(f"Value ({self.value_id.name}) does not correspond to category ({self.category_id.name})")

####################

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    total_purchased = models.DecimalField(max_digits=10, decimal_places=2, editable=False, blank=True, null=True)

    def __str__(self):
        return self.nombre
    class Meta:

        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['name']
    
    def __str__(self) -> str:

        return f"{self.name}, {self.phone_number}"


class Stock(models.Model):
    
    article_id = models.OneToOneField(Article,verbose_name="Article", on_delete=models.CASCADE)
    stock = models.PositiveSmallIntegerField(verbose_name="Stock", default=0) #Value from 0 to 32767
    
    class Meta:

        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        ordering = ['article_id','stock']
    
    def __str__(self) -> str:

        return f"{self.article_id.name}, {self.stock}"


class Promotion(models.Model):
    
    name = models.CharField(verbose_name="Name",max_length=100, unique=True)
    article_id = models.ManyToManyField(Article, verbose_name="Articles", through="ArticlePromotion")
    discount = models.DecimalField(verbose_name="Discount", max_digits=3, decimal_places=2, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    sell_price = models.DecimalField(verbose_name="$ SALE", max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    remainder = models.SmallIntegerField(verbose_name="Remaining amount", blank=True, null=True)
    class Meta:

        
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
        ordering = ['sell_price']
    
    def __str__(self) -> str:

        return f"{self.promotion_name}, {self.article_id}, {self.discount}, {self.sell_price}"

class ArticlePromotion(models.Model):
    article_id = models.ForeignKey(Article,on_delete=models.CASCADE)
    promotion_id = models.ForeignKey(Promotion, on_delete=models.CASCADE)

class Order(models.Model):

    customer_id = models.ForeignKey(Customer,verbose_name="Customer", on_delete=models.CASCADE)
    article_id = models.ManyToManyField(Article, verbose_name="Articles", through="ArticleOrder")
    article_quantity = models.PositiveSmallIntegerField(verbose_name="Articles Quantity", editable=False, blank=True, null=True)
    total_pay = models.DecimalField(verbose_name="Total pay", max_digits=10, decimal_places=2, editable=False, blank=True, null=True)
    details = models.TextField(verbose_name="Details", blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation date", editable=False)
    updated_date = models.DateTimeField(auto_now=True,verbose_name="Date last modified", editable=False)
    delivery_status = models.BooleanField(verbose_name="Delivery status", default=False)

    class Meta:

        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['customer_id',]
    
    def __str__(self) -> str:

        return f"name: {self.customer_id.name}, phone: {self.customer_id.phone_number}, total: {self.total_pay}, status: {self.delivery_status}"


class ArticleOrder(models.Model):
    article_id = models.ForeignKey(Article,on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)


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

