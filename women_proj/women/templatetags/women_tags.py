from django import template
from women.models import Category, Tag

register = template.Library()
categories = Category.objects.all()


@register.simple_tag()
def get_categories():
    return categories


@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    return {'tags': Tag.objects.all()}
