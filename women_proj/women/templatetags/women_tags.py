from django import template
from women.models import Category, Tag
from django.db.models import Count
from women.utils import menu

register = template.Library()


@register.simple_tag()
def get_menu():
    return menu


@register.simple_tag()
def get_categories():
    res = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    return res.order_by('id')


@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    return {'tags': Tag.objects.annotate(total=Count('woman')).filter(total__gt=0)}
