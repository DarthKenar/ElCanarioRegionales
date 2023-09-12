from django import template
from ..models import Category
from messageslog.models import MessageLog

register = template.Library()
from authentication.models import UserProfileExtends
@register.filter
def filter_by_category(values, category):
    return [value for value in values if value.category_id == category] #used list comprehension becouse its more elegant

@register.simple_tag
def get_all_categories():
    categories = Category.objects.all()
    return categories

@register.simple_tag
def get_user_picture(user):
    try:
        user_profile = UserProfileExtends.objects.get(user=user)
        return user_profile.profile_picture.url if user_profile.profile_picture else ''
    except UserProfileExtends.DoesNotExist:
        return ""
        
@register.simple_tag
def get_all_messageslog():
    try:
        messages = MessageLog.objects.all()
        return messages
    except Exception as e:
        print(f"Error Exception: {e}")

@register.simple_tag
def hx_post_update_customers_render_field(object_id, true_or_false):
    return f"hx-post=/customers/update/{object_id}/{true_or_false}"


@register.simple_tag
def hx_post_create_customers_render_field(true_or_false):
    return f"hx-post=/customers/create/{true_or_false}"

@register.simple_tag
def hx_post_update_orders_render_field(object_id, true_or_false):
    return f"hx-post=/orders/update/{object_id}/{true_or_false}"


@register.simple_tag
def hx_post_create_orders_render_field(true_or_false):
    return f"hx-post=/orders/create/{true_or_false}"

@register.simple_tag
def trigger_input():
    return "hx-trigger=keyup&nbsp;changed&nbsp;delay:300ms"