from django import template
from core.models import Myorder

register = template.Library()


@register.filter
def myorder_item_count(user):
    if user.is_authenticated:
        qs = Myorder.objects.filter(user=user)
        if qs.exists():
            return len(qs)
    return 0
