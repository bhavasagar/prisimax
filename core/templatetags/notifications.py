from django import template
from django.contrib.auth.models import User
from core.models import Notification

register = template.Library()


@register.simple_tag
def notifications(request,id):
    value = request.COOKIES.get('seen')
    if value is None:        
        notes = Notification.objects.filter(type="A")    
        if id != 0:
            user = False
            try:
                user = User.objects.filter(id=id)
            except:
                pass
            if user:
                note_user = Notification.objects.filter(users__in=user)
                notes = notes | note_user
        return notes   
    return False 
