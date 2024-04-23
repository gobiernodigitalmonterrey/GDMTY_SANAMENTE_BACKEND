from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter()
@stringfilter
def add_class_to_richtext_embeds(value):
    """Agregar class responsiva al iframe de los embeds/incrustaciones de video"""
    return value.replace('<iframe', '<div class=\"custom-embed\"><iframe').replace('</iframe>', '</iframe></div>')
