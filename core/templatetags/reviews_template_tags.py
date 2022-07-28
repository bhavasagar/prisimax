from django import template
from core.models import Review

register = template.Library()

 
@register.filter
def review_count(item):
    qs = Review.objects.filter(item=item)
    if qs.exists():
        return len(qs)
    return 0


@register.filter
def scale_hund(rating):    
    return round((float(rating)*100)/10,1)