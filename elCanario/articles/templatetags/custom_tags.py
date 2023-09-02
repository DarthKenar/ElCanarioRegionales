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
