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
    name = models.CharField(verbose_name="Name",max_length=100)
    image = models.ImageField(upload_to="articles", null=True, blank=True)
    characteristics_id = models.ManyToManyField(Value,related_name='characteristics_id', blank=True, through='ArticleValue')
    buy_price = models.DecimalField(verbose_name="Buy price", max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    increase = models.DecimalField(verbose_name="Increment", max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    sell_price = models.DecimalField(verbose_name="Sell price", max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    stock = models.PositiveSmallIntegerField(verbose_name="Stock") #Value from 0 to 32767

    def __str__(self) -> str:
        return f"{self.pk}, {self.name}, {self.sell_price}"

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


