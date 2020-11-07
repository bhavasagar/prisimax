from django import template
from core.models import Order
from datetime import timedelta
import random

register = template.Library()


@register.filter
def add_xdays(d):
    return d+timedelta(days=random.randint(1,3))
