from django.utils.safestring import mark_safe
from wagtail import hooks


@hooks.register('insert_editor_css')
def editor_css():
    """Insertar hoja de estilo (inline) que muestra OSM Widget correctamente. Bug: originario de la librería"""

    return '<style>#panel-child-contenido-geom-content .w-field__wrapper {height: 400px;}</style>'


@hooks.register('insert_editor_js')
def editor_js():
    """
    Insertar script (inline) que provoca un 'resize' para forzar un refersh al OSM Widget y muestre las tiles
    correctamente.
    Bug: originario de la librería:
    """

    return mark_safe(
        '<script>window.addEventListener("DOMContentLoaded", (event) => { window.dispatchEvent(new Event("resize")) '
        '})</script>'
    )