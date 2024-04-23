from django import template
from sanamente.snippets import Color

register = template.Library()


@register.filter(name="index_color_filter", is_safe=True)
def add_class_to_index_filter(value):
    index = len(value)
    for val in value:
        if Color.objects.filter(nombre=val).exists() or str(val) == 'None':
            index -= 1

    return index
