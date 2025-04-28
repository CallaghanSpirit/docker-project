from django import template
import goods.views as views
from goods.models import Category, Tags
from django.db.models import Count

register = template.Library()

@register.inclusion_tag('goods/list_categories.html')
def show_categories():
    cats = Category.objects.annotate(total=Count('goods')).filter(total__gt=0)
    return {'cats':cats}

@register.inclusion_tag('goods/list_tags.html')
def show_tags():
    tags = Tags.objects.filter(gtags__gt=0)
    return {'tags': Tags.objects.all() }

