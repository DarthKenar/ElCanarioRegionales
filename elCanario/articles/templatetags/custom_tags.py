from django import template
from ..models import Category
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