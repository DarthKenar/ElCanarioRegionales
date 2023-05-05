from django import template

register = template.Library()

@register.filter
def filter_by_category(values, category):
    return [value for value in values if value.category_id == category] #used list comprehension becouse its more elegant
