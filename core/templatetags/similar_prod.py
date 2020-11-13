from django import template
from core.models import Item
from django.db.models import Q
register = template.Library()

@register.simple_tag
def similar_prod(item):
    qs = Item.objects.filter(Q(title__search=item.title) | Q(category__search=item.category)).exclude(id=item.id).order_by('-id')
    if qs.count() < 12:
        ns = Item.objects.filter(category=item.category)
        qs = qs | ns
    return qs[0:12]
    