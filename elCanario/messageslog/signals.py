#https://refactoring.guru/es/design-patterns/mediator/python/example#example-0
from messageslog.models import MessageLog
from articles.models import Article, Category, Value
from customers.models import Customer
from orders.models import Order
from django.db.models.signals import post_save, post_delete
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver

#https://docs.djangoproject.com/en/4.2/topics/signals/#connecting-to-signals-sent-by-specific-senders

#! Articles

@receiver(post_save, sender=Article)
def create_messages_log_on_article_create(sender, instance, created, **kwargs):
    #created is true when an article is created
    if created:
        MessageLog.objects.create(info=_(f"Article created: {instance}"))

@receiver(post_save, sender=Article)
def create_messages_log_on_article_update(sender, instance, created, **kwargs):
    #created is false when an article is updated
    if not created:
        MessageLog.objects.create(info=_(f"Article updated: {instance}"))

@receiver(post_delete, sender=Article)
def create_messages_log_on_article_delete(sender, instance, **kwargs):
    MessageLog.objects.create(info=_(f"Article deleted: {instance}"))

#! Categories

@receiver(post_save, sender=Category)
def create_messages_log_on_category_create(sender, instance, created, **kwargs):
    if created:
        MessageLog.objects.create(info=_(f"Category created: {instance}"))

@receiver(post_save, sender=Category)
def create_messages_log_on_category_update(sender, instance, created, **kwargs):
    if not created:
        MessageLog.objects.create(info=_(f"Category updated: {instance}"))

@receiver(post_delete, sender=Category)
def create_messages_log_on_category_delete(sender, instance, **kwargs):
    MessageLog.objects.create(info=_(f"Category deleted: {instance}"))

#! Values

@receiver(post_save, sender=Value)
def create_messages_log_on_value_create(sender, instance, created, **kwargs):
    if created:
        MessageLog.objects.create(info=_(f"Value created: {instance}"))

@receiver(post_save, sender=Value)
def create_messages_log_on_value_update(sender, instance, created, **kwargs):
    if not created:
        MessageLog.objects.create(info=_(f"Value updated: {instance}"))

@receiver(post_delete, sender=Value)
def create_messages_log_on_value_delete(sender, instance, **kwargs):
    MessageLog.objects.create(info=_(f"Value deleted: {instance}"))

#! Customers

@receiver(post_save, sender=Customer)
def create_messages_log_on_customer_create(sender, instance, created, **kwargs):
    if created:
        MessageLog.objects.create(info=_(f"Customer created: {instance}"))

@receiver(post_save, sender=Customer)
def create_messages_log_on_customer_update(sender, instance, created, **kwargs):
    if not created:
        MessageLog.objects.create(info=_(f"Customer updated: {instance}"))

@receiver(post_delete, sender=Customer)
def create_messages_log_on_customer_delete(sender, instance, **kwargs):
    MessageLog.objects.create(info=_(f"Customer deleted: {instance}"))

#! Orders

@receiver(post_save, sender=Order)
def create_messages_log_on_order_create(sender, instance, created, **kwargs):
    if created:
        MessageLog.objects.create(info=_(f"Order created: {instance}"))

@receiver(post_save, sender=Order)
def create_messages_log_on_order_update(sender, instance, created, **kwargs):
    if not created:
        MessageLog.objects.create(info=_(f"Order updated: {instance}"))

@receiver(post_delete, sender=Order)
def create_messages_log_on_order_delete(sender, instance, **kwargs):
    MessageLog.objects.create(info=_(f"Order deleted: {instance}"))