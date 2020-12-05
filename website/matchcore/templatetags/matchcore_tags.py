from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def is_active_un(request, url, un):
    if request.path in reverse(url, args=[un]): #fixme
        return "active"
    return ""

@register.simple_tag
def is_active(request, url):
    if request.path in reverse(url): #fixme
        return "active"
    return ""