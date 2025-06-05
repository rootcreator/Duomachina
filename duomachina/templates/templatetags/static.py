from django import template
from django.templatetags.static import static as django_static

register = template.Library()
 
@register.simple_tag
def static(path):
    return django_static(path) 