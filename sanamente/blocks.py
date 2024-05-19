from wagtail import blocks as core_blocks
from wagtail.snippets import blocks as snippet_blocks
from wagtail.rich_text import expand_db_html
from threadlocals.threadlocals import get_current_request
from wagtail.images import blocks as image_blocks
from .snippets import Color, Icono
from wagtail.models import Site
from django.utils.html import escape

# Create your blocks here.


class ImagenAvatarChooserBlock(image_blocks.ImageChooserBlock):

    def get_api_representation(self, instance, context=None):
        if instance:
            return {
                'id': instance.id,
                'title': instance.title,
                "meta": {
                    "type": "wagtailimages.Image",
                    'medium': instance.get_rendition('fill-200x200').attrs_dict,
                    'small': instance.get_rendition('fill-100x100').attrs_dict,
                }
            }


class RichTextBlock(core_blocks.RichTextBlock):

    def get_api_representation(self, instance, context=None):
        get_api_representation = super().get_api_representation(instance)
        representation = expand_db_html(get_api_representation)

        """
        request = get_current_request()
        site = Site.find_for_request(request)
        root_url = site.root_url if site else ''
        representation = representation.replace('src="/', f'src="{root_url}/').replace('\n', '') \
            .replace('href="/', f'href="{root_url}/') \
            .replace('<div>    <iframe', '<div class=\"custom-embed\"><iframe')
        return representation
        """

        # Obtén el contexto si es posible
        if context:
            # Busca la página actual en el contexto
            page = context.get('page')

            # Si tienes acceso a la página actual
            if page:
                # Obtiene el sitio asociado con la página actual
                site = Site.find_for_request(page.get_request())

                # Obtiene la URL raíz del sitio
                root_url = site.root_url if site else ''

                # Escapa la URL raíz para evitar problemas de seguridad
                root_url_escaped = escape(root_url)

                # Realiza las modificaciones necesarias en la representación del API
                representation = representation.replace('src="/', f'src="{root_url_escaped}/').replace('\n', '') \
                    .replace('href="/', f'href="{root_url_escaped}/') \
                    .replace('<div>    <iframe', '<div class=\"custom-embed\"><iframe')

        return representation


class TarjetaImagenBlock(core_blocks.StreamBlock):
    imagen = image_blocks.ImageChooserBlock(
        label='Imagen', required=True, max_num=1
    )
    titulo = core_blocks.RichTextBlock(required=False,
                                       features=['bold', 'italic', 'superscript', 'subscript', 'strikethrough'],
                                       max_num=1)
    contenido = core_blocks.RichTextBlock(required=True,
                                          features=['bold', 'italic', 'superscript', 'subscript', 'strikethrough',
                                                    'link'],
                                          max_num=1)

    class Meta:
        icon = 'image'
        block_counts = {
            'imagen': {'min_num': 1, 'max_num': 1},
            'titulo': {'min_num': 1, 'max_num': 1},
            'contenido': {'min_num': 1, 'max_num': 1},
        }
        label = "Tarjeta con imagen"


class TarjetaTextoEnriquecidoBlock(core_blocks.StreamBlock):
    titulo = core_blocks.RichTextBlock(required=False,
                                       features=['bold', 'italic', 'superscript', 'subscript', 'strikethrough'],
                                       max_num=1)
    contenido = core_blocks.RichTextBlock(required=True,
                                          features=['bold', 'italic', 'superscript', 'subscript', 'strikethrough',
                                                    'link'],
                                          max_num=1)

    class Meta:
        icon = 'image'
        block_counts = {
            'titulo': {'min_num': 1, 'max_num': 1},
            'contenido': {'min_num': 1, 'max_num': 1},
        }
        label = "Tarjeta con texto marcado"


class TabBlock(core_blocks.StructBlock):
    etiqueta = core_blocks.CharBlock(max_length=40)
    contenido = core_blocks.RichTextBlock(required=False,
                                          features=['bold', 'italic', 'h2', 'h3', 'h4', 'h5', 'superscript',
                                                    'subscript', 'strikethrough', 'ol', 'ul', 'link', 'image',
                                                    'document-link', 'embed', 'blockquote'],
                                          )

    class Meta:
        icon = 'fa-camera-retro'
        label = 'Tab'


class TabsBlock(core_blocks.StreamBlock):
    tab = TabBlock()

    class Meta:
        icon = 'tabs'
        label = 'Tabs'


class ItemExpandibleBlock(core_blocks.StructBlock):
    icono = snippet_blocks.SnippetChooserBlock(Icono, required=False)
    titulo = core_blocks.CharBlock(max_length=100)
    subtitulo = core_blocks.CharBlock(max_length=100)
    texto_marcado = core_blocks.RichTextBlock(required=False,
                                              features=['bold', 'italic', 'h2', 'h3', 'h4', 'h5', 'superscript',
                                                        'subscript', 'strikethrough', 'ol', 'ul', 'link', 'image',
                                                        'document-link', 'embed', 'blockquote'],
                                              )

    class Meta:
        icon = 'mdi-row'
        label = 'Item Expandible'


class ExpandibleBlock(core_blocks.StreamBlock):
    item = TabBlock()

    class Meta:
        icon = 'mdi-file'
        label = 'Expandible'


class EventoLineaTiempo(core_blocks.StructBlock):
    titulo = core_blocks.CharBlock(max_length=40)
    subtitulo = core_blocks.CharBlock(max_length=40, required=False)
    contenido = core_blocks.RichTextBlock(required=False,
                                          features=['bold', 'italic', 'h4', 'h5', 'superscript',
                                                    'subscript', 'strikethrough', 'ol', 'ul', 'link', 'image',
                                                    'document-link', 'embed', 'blockquote'])
    color = snippet_blocks.SnippetChooserBlock(Color, required=False)
    icono = snippet_blocks.SnippetChooserBlock(Icono, required=False)
    avatar = ImagenAvatarChooserBlock(
        label='Avatar', required=False
    )

    class Meta:
        icon = 'time'
        label = 'Evento de línea de tiempo'


class LineaTiempoBlock(core_blocks.StreamBlock):
    evento = EventoLineaTiempo()

    class Meta:
        icon = 'clock'
        label = 'Linea de tiempo'


class BotonAccionBlock(core_blocks.StructBlock):
    accion_tipo = core_blocks.ChoiceBlock(required=True, choices=(
        ('', 'Tipo de acción'), ('sin_accion', 'Sin acción'), ('pagina', 'Página'), ('url', 'URL')),
                                          classname='wagtailuiplus__choice-handler '
                                                    'wagtailuiplus__choice-handler--accion_tipo')
    accion_pagina = core_blocks.PageChooserBlock(required=False,
                                                 classname='wagtailuiplus__choice-handler-target--accion_tipo '
                                                           'wagtailuiplus__choice-handler-hidden-if--url '
                                                           'wagtailuiplus__choice-handler-hidden-if--ancla')
    accion_url = core_blocks.URLBlock(required=False,
                                      classname='wagtailuiplus__choice-handler-target--accion_tipo '
                                                'wagtailuiplus__choice-handler-hidden-if--pagina '
                                                'wagtailuiplus__choice-handler-hidden-if--ancla')
    accion_texto = core_blocks.CharBlock(max_length=30, required=False)
    accion_clase = snippet_blocks.SnippetChooserBlock(Color, required=False)
    accion_alineacion = core_blocks.ChoiceBlock(max_length=30, null=True, blank=True, default='izquierda',
                                                choices=(('', 'Alineación'), ('izquierda', 'Izquierda'),
                                                         ('centro', 'Centro'), ('derecha', 'Derecha')))
    icono = snippet_blocks.SnippetChooserBlock(Icono, required=False)
    icono_posicion = core_blocks.ChoiceBlock(max_length=30, null=True, blank=True, default='izquierda',
                                             choices=(('izquierda', 'Izquierda'), ('derecha', 'Derecha')))
