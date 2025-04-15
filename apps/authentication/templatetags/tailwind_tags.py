from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def tailwind_cdn():
    return mark_safe(
        '<script src="https://cdn.tailwindcss.com"></script>'
    )