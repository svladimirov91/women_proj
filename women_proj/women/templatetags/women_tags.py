from django import template
from women.models import Category, Tag
from django.db.models import Count

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.annotate(total=Count('posts')).filter(total__gt=0)


@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    return {'tags': Tag.objects.annotate(total=Count('woman')).filter(total__gt=0)}
