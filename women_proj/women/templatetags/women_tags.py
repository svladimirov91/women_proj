from django import template
from women.models import Category

register = template.Library()
categories = Category.objects.all()


@register.simple_tag()
def get_categories():
    return categories
