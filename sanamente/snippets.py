from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.api import APIField
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from . import wagtail_serializers as sanamente_serializers

#

@register_snippet
class Color(models.Model):
    nombre = models.CharField(max_length=120, primary_key=True)

    api_fields = [
        APIField("nombre"),
    ]

    def __str__(self):
        return self.nombre


@register_snippet
class Icono(models.Model):
    nombre = models.CharField(max_length=120, primary_key=True)

    api_fields = [
        APIField("nombre"),
    ]

    def __str__(self):
        return self.nombre


@register_snippet
class BiografiaAutor(models.Model):
    """Modelo/snippet Biografía y perfil de usuario para página tipo blog. """

    nombre = models.CharField(max_length=120, unique=True)
    avatar = models.ForeignKey('wagtailimages.Image', on_delete=models.PROTECT, related_name='+', null=True, blank=True)
    biografia_autor = RichTextField(features=['bold', 'italic', 'superscript', 'subscript', 'strikethrough'],
                                    max_length=255, null=True, blank=True)

    """ Paneles de los campos del snippet. """
    panels = [
        FieldPanel('nombre'),
        FieldPanel('avatar'),
        FieldPanel('biografia_autor'),
    ]

    """ API Fields: Propiedades que se exponen en el endpoint de la API Rest. """
    api_fields = [
        APIField("nombre"),
        APIField("avatar", serializer=sanamente_serializers.ImagenXsSerializer()),
        APIField("biografia_autor"),
    ]

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Biografía de autor"
        verbose_name_plural = "Biografías de autor"

