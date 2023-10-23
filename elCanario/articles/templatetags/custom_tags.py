from django import template
from ..models import Category
from messageslog.models import MessageLog

register = template.Library()
@register.filter
def filter_by_category(values, category):
    return [value for value in values if value.category_id == category] #used list comprehension becouse its more elegant

@register.simple_tag
def get_all_categories():
    categories = Category.objects.all()
    return categories

        
@register.simple_tag
def get_all_messageslog():
    try:
        messages = MessageLog.objects.all()
        return messages
    except Exception as e:
        print(f"Error Exception: {e}")

@register.simple_tag
def hx_post_update_customers_render_field(object_id):
    return f"customers:update {object_id}"


@register.simple_tag
def hx_post_create_customers_render_field():
    return f"customers:create"

@register.simple_tag
def hx_post_update_orders_render_field(object_id):
    return f"orders:update {object_id}"


@register.simple_tag
def hx_post_create_orders_render_field():
    return f"orders:create"

@register.simple_tag
def trigger_input():
    return "hx-trigger=keyup&nbsp;changed&nbsp;delay:300ms"
