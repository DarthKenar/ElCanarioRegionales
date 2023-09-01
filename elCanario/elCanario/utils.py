# from django.shortcuts import get_object_or_404
# from articles.models import Categories, Colors, Sizes, Materials
from typing import Tuple, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from articles.models import Category, Value, ArticleValue, Article
from customers.models import Customer
import re
@login_required
def render_login_required(request: object, template: str,context: dict) -> HttpResponse: 
    """This function is used for all functions that require the user to be logged in."""
    return render(request, template, context)

def string_is_empty(s:str)-> bool:
    """Returns True if the string is empty or contains only blanks.

    Args:
        s (str): string, field to check

    Returns:
        bool: verification (true if the string is empty or contains only blanks.)
    """

    return s is None or s.strip() == ''

