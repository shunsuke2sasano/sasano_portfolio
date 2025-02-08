from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def add_attrs(field, attrs):
    attrs = dict(attr.split(':') for attr in attrs.split(','))
    return field.as_widget(attrs=attrs)
