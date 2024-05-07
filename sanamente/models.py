from django.contrib.gis.db import models
from wagtail import fields as core_fields
from wagtail.models import Page
from wagtail.api import APIField
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import TabbedInterface, ObjectList
from wagtail.snippets.models import register_snippet
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail import fields as wagtail_fields
from . import blocks as sanamente_blocks
from .snippets import BiografiaAutor
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from . import wagtail_serializers as sanamente_serializers
from django.contrib.gis.forms.widgets import OSMWidget
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL
register_snippet(Tag)


# Mixins
class ImagenPrincipalMixin(models.Model):
    """
    Mixin: imagen principal.
    Atributos
    ----------
    imagen_principal - FK:
        Llave foránea que refiere a una imagen que se usa como portada, en miniaturas, y en metadatos de SEO.
    mostrar_imagen_principal - bool:
        Checkbox para mostrar la imagen principal como portada. (default False)
    """

    imagen_principal = models.ForeignKey('wagtailimages.Image', on_delete=models.PROTECT, related_name='+')
    mostrar_imagen_principal = models.BooleanField(default=False)

    """ API Fields: Propiedades que se exponen en el endpoint de la API Rest. """
    api_fields = [
        APIField("imagen_principal", serializer=sanamente_serializers.ImagenLgSerializer()),
        APIField("mostrar_imagen_principal"),
    ]

    """ Panel contenido: Muestra propiedades de la clase bajo el panel de contenido. """
    content_panels = [
        FieldPanel("imagen_principal"),
    ]

    """ Panel promocionar: Muestra propiedades de la clase bajo el panel de promocionar. """
    promote_panels = [
        FieldPanel("mostrar_imagen_principal"),
    ]

    class Meta:
        """Abstract Model. - Mixin"""
        abstract = True


class AutorMixin(models.Model):
    """ Mixin para autor que puede ser utilizado en Entrada de blog. """
    autor = models.ForeignKey(BiografiaAutor, blank=True, null=True, on_delete=models.PROTECT)

    autor_panels = [
        FieldPanel("autor")
    ]

    class Meta:
        """Abstract Model. - Mixin"""
        abstract = True


class PaginaBaseAbstracta(Page):
    """PaginaBaseAbstracta"""
    intro = wagtail_fields.RichTextField(features=['bold', 'italic', 'superscript', 'subscript', 'strikethrough'])
    contenido = core_fields.StreamField([
        ('texto_enriquecido', sanamente_blocks.RichTextBlock()),
        ('tabs', sanamente_blocks.TabsBlock()),
        ('expandible', sanamente_blocks.ExpandibleBlock()),
        ('linea_tiempo', sanamente_blocks.LineaTiempoBlock()),
        ('boton_accion', sanamente_blocks.BotonAccionBlock())
    ], blank=False, use_json_field=True, verbose_name='Contenido del cuerpo de la página')

    api_fields = [
        APIField("title"),
        APIField("intro"),
        APIField("contenido")
    ]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("contenido")
    ]

    class Meta:
        abstract = True


class PaginaRaiz(Page):
    subpage_types = ['PaginaGrupoNumeroTelefonicoEmergencia', 'PaginaGrupoServicioProfesional',
                     'PaginaGrupoActividadBienestar', 'PaginaGrupoBlog']
    parent_page_types = ['wagtailcore.Page']

    class Meta:
        verbose_name = "Raiz"
        verbose_name_plural = "Raiz"


class PaginaGrupoNumeroTelefonicoEmergencia(Page):
    subpages_types = ['NumeroTelefonicoEmergencia']
    parent_page_types = ['PaginaRaiz']

    max_count_per_parent = 1

    class Meta:
        verbose_name = "Números telefónicos de emergencia"
        verbose_name_plural = "Números telefónicos de emergencia"


class PaginaGrupoServicioProfesional(Page):
    subpages_types = ['Servicio']
    parent_page_types = ['PaginaRaiz']

    max_count_per_parent = 1

    class Meta:
        verbose_name = "Servicios profesionales"
        verbose_name_plural = "Servicios profesionales"


class PaginaGrupoActividadBienestar(Page):
    subpages_types = ['ActividadBienestar']
    parent_page_types = ['PaginaRaiz']

    max_count_per_parent = 1

    class Meta:
        verbose_name = "Actividades de bienestar"
        verbose_name_plural = "Actividades de bienestar"


@register_snippet
class NumeroTelefonicoEmergenciaEtiqueta(TaggedItemBase):
    content_object = ParentalKey('NumeroTelefonicoEmergencia', on_delete=models.CASCADE, related_name='tagged_items')


class NumeroTelefonicoEmergencia(PaginaBaseAbstracta):
    subpage_types = []
    parent_page_types = ['PaginaGrupoNumeroTelefonicoEmergencia']

    etiquetas = ClusterTaggableManager(through=NumeroTelefonicoEmergenciaEtiqueta, blank=True)
    telefono = models.CharField(max_length=10,
                                validators=[
                                    RegexValidator('^([09]{1}\d{2}|[1-9]{1}\d{9})$',
                                                   message='Debe tener 3 o 10 dígitos y ser un número telefónico válido')],
                                verbose_name='Número telefónico')

    api_fields = PaginaBaseAbstracta.api_fields + [
        APIField("telefono"),
        APIField("etiquetas")
    ]

    content_panels = PaginaBaseAbstracta.content_panels + [
        FieldPanel("telefono"),
        FieldPanel("etiquetas")
    ]

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "Número telefónico de emergencia"
        verbose_name_plural = "Números telefónicos de emergencia"


@register_snippet
class CategoriaActividadBienestar(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoria de actividad de bienestar"
        verbose_name_plural = "Categorias de actividades de bienestar"


@register_snippet
class ActividadBienestarEtiqueta(TaggedItemBase):
    content_object = ParentalKey('ActividadBienestar', on_delete=models.CASCADE, related_name='tagged_items')

    def __save__(self, *args, **kwargs):
        self.tag.name = self.tag.name.lower()
        super(ActividadBienestarEtiqueta, self).save(*args, **kwargs)


class ActividadBienestar(PaginaBaseAbstracta):
    subpage_types = []
    parent_page_types = ['PaginaGrupoActividadBienestar']

    imagen = models.ForeignKey('wagtailimages.Image', on_delete=models.PROTECT)
    categoria = models.ForeignKey(CategoriaActividadBienestar, on_delete=models.PROTECT)
    etiquetas = ClusterTaggableManager(through=ActividadBienestarEtiqueta, blank=True)

    api_fields = PaginaBaseAbstracta.api_fields + [
        APIField("categoria", serializer=sanamente_serializers.CharFieldNombreSerializer()),
        APIField("etiquetas"),
        APIField("imagen", serializer=sanamente_serializers.ImagenMdSerializer()),
    ]

    content_panels = PaginaBaseAbstracta.content_panels + [
        FieldPanel("categoria", heading="Catégoria"),
        FieldPanel("etiquetas"),
        FieldPanel("imagen"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Actividad de bienestar"
        verbose_name_plural = "Actividades de bienestar"


class ActividadBienestarFavorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    actividad = models.ForeignKey("ActividadBienestar", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} - {self.actividad}"

    class Meta:
        verbose_name = "Actividad de bienestar favorita"
        verbose_name_plural = "Actividades de bienestar favoritas"


class ActividadBienestarValoracion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    actividad = models.ForeignKey(ActividadBienestar, on_delete=models.CASCADE)
    valoracion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.usuario} - {self.actividad} - {self.valoracion}"

    class Meta:
        verbose_name = "Valoración de actividad de bienestar"
        verbose_name_plural = "Valoraciones de actividades de bienestar"


@register_snippet
class CategoriaServicioProfesional(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoria de servicios"
        verbose_name_plural = "Categorias de servicios"


@register_snippet
class EspecialidadServicioProfesional(models.Model):
    nombre = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Especialidad de servicios"
        verbose_name_plural = "Especialidades de servicios"


@register_snippet
class ModalidadServicioProfesional(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Modalidad de servicios"
        verbose_name_plural = "Modalidades de servicios"


@register_snippet
class ServicioProfesionalEtiqueta(TaggedItemBase):
    content_object = ParentalKey('ServicioProfesional', on_delete=models.CASCADE, related_name='tagged_items')


class ServicioProfesional(PaginaBaseAbstracta):
    subpage_types = []
    parent_page_types = ['PaginaGrupoServicioProfesional']

    categoria = models.ForeignKey(CategoriaServicioProfesional, on_delete=models.PROTECT)
    especialidad = models.ForeignKey(EspecialidadServicioProfesional, on_delete=models.PROTECT)
    etiquetas = ClusterTaggableManager(through=ServicioProfesionalEtiqueta, blank=True)
    fotografia = models.ForeignKey('wagtailimages.Image', on_delete=models.PROTECT,
                                   related_name='+')
    areas_experiencia = core_fields.RichTextField(
        features=['bold', 'italic', 'superscript', 'subscript', 'strikethrough', 'ol', 'ul', 'hr', 'link'])
    telefono = models.CharField(max_length=10,
                                validators=[
                                    RegexValidator('^([09]{1}\d{2}|[1-9]{1}\d{9})$',
                                                   message='Debe tener 3 o 10 dígitos y ser un número telefónico válido')],
                                verbose_name='Número telefónico')
    modalidad = models.ForeignKey(ModalidadServicioProfesional, on_delete=models.PROTECT)
    domicilio = models.CharField(max_length=255, null=True, blank=True)
    geom = models.PointField(srid=3857, null=True, blank=True, verbose_name="Ubicación geográfica")
    es_servicio_publico = models.BooleanField(default=False)
    precio_minimo = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    precio_maximo = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cedula_profesional = models.CharField(max_length=8, validators=[RegexValidator('^\d{8}$', message='Debe tener 8 dígitos')])

    def __str__(self):
        return self.title

    api_fields = PaginaBaseAbstracta.api_fields + [
        APIField("categoria", serializer=sanamente_serializers.CharFieldNombreSerializer()),
        APIField("especialidad", serializer=sanamente_serializers.CharFieldNombreSerializer()),
        APIField("etiquetas"),
        APIField("fotografia", serializer=sanamente_serializers.ImagenFotografia()),
        APIField("areas_experiencia"),
        APIField("telefono"),
        APIField("modalidad", serializer=sanamente_serializers.CharFieldNombreSerializer()),
        APIField("domicilio"),
        APIField("geom", serializer=sanamente_serializers.Geom3857to4326Serializer()),
        APIField("es_servicio_publico"),
        APIField("precio_minimo"),
        APIField("precio_maximo"),
        APIField("cedula_profesional"),
    ]

    content_panels = PaginaBaseAbstracta.content_panels + [
        FieldPanel("categoria", heading="Categoría"),
        FieldPanel("especialidad"),
        FieldPanel("etiquetas"),
        FieldPanel("fotografia", heading="Fotografía"),
        FieldPanel("areas_experiencia", heading="Áreas de experiencia"),
        FieldPanel("telefono"),
        FieldPanel("modalidad"),
        FieldPanel("domicilio"),
        FieldPanel("cedula_profesional", heading="Cédula profesional"),
        FieldPanel("es_servicio_publico", heading="Es servicio público"),
        FieldPanel("precio_minimo", heading="Precio mínimo"),
        FieldPanel("precio_maximo", heading="Precio máximo"),
        FieldPanel("geom", classname="geom",
                   widget=OSMWidget(attrs={'default_lon': -100.31, 'default_lat': 25.66, 'default_zoom': 11})),
    ]

    class Meta:
        verbose_name = "Servicio profesional"
        verbose_name_plural = "Servicios profesionales"


class ServicioProfesionalFavorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    servicio = models.ForeignKey(ServicioProfesional, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} - {self.servicio}"

    class Meta:
        verbose_name = "Servicio profesional favorita"
        verbose_name_plural = "servicios profesional favoritos"


class ServicioProfesionalValoracion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    servicio = models.ForeignKey(ServicioProfesional, on_delete=models.CASCADE)
    valoracion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.usuario} - {self.servicio} - {self.valoracion}"

    class Meta:
        verbose_name = "Valoracion de servicio profesional"
        verbose_name_plural = "Valoraciones de servicios profesionales"



@register_snippet
class CategoriaEntradaBlog(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría de entradas de blog"
        verbose_name_plural = "Categorías de entradas de blog"


@register_snippet
class EntradaBlogEtiqueta(TaggedItemBase):
    """
    Etiqueta para páginas Entrada de blog.
    ----------
    """
    content_object = ParentalKey('EntradaBlog', on_delete=models.CASCADE, related_name='tagged_items')

    def __save__(self, *args, **kwargs):
        self.tag.name = self.tag.name.lower()
        super(EntradaBlogEtiqueta, self).save(*args, **kwargs)


class PaginaGrupoBlog(Page):
    """
    Página (sin contenido) para agrupar páginas de tipo EntradaBlog, para organizar el árbol, y para mostrar en menús.
    ----------
    """
    subpage_types = ['EntradaBlog']
    parent_page_types = ['PaginaRaiz']

    """ Panel contenido: Muestra propiedades de la clase bajo el panel de contenido. """
    content_panels = Page.content_panels

    """ Panel promocionar: Muestra propiedades de la clase bajo el panel de promocionar. """
    promote_panels = Page.promote_panels

    max_count_per_parent = 1

    def save(self, *args, **kwargs):
        if self.title == self.title.upper():
            self.title = self.title.capitalize()
        super(PaginaGrupoBlog, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Entradas de blog"
        verbose_name_plural = "Entradas de blog"


class EntradaBlog(PaginaBaseAbstracta, ImagenPrincipalMixin, AutorMixin):
    subpage_types = []
    parent_page_types = ['PaginaGrupoBlog']

    categoria = models.ForeignKey(CategoriaEntradaBlog, on_delete=models.PROTECT)
    etiquetas = ClusterTaggableManager(through=EntradaBlogEtiqueta, blank=True)

    """ API Fields: Propiedades que se exponen en el endpoint de la API Rest. """
    api_fields = ImagenPrincipalMixin.api_fields + [
        APIField("title"),
        APIField("autor", serializer=sanamente_serializers.AutorBioSerializer()),
        APIField("intro"),
        APIField("categoria", serializer=sanamente_serializers.CharFieldNombreSerializer()),
        APIField("contenido"),
        APIField("etiquetas"),
    ]

    """ Panel contenido: Muestra propiedades de la clase bajo el panel de contenido. """
    content_panels = Page.content_panels + \
        ImagenPrincipalMixin.content_panels + \
        [
            FieldPanel('intro'),
            FieldPanel('categoria', heading="Catégoria"),
            FieldPanel('contenido'),
            FieldPanel('etiquetas'),
        ]

    """ Panel promocionar: Muestra propiedades de la clase bajo el panel de promocionar. """
    promote_panels = Page.promote_panels + \
        ImagenPrincipalMixin.promote_panels

    """ Panel para editar información del autor del post"""
    autor_panels = AutorMixin.autor_panels

    # Agrega una tab el admin de wagtail.
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Contenido'),
        ObjectList(promote_panels, heading='Promocionar'),
        ObjectList(autor_panels, heading='Información del autor'),
    ])

    class Meta:
        verbose_name = "Entrada de blog"
        verbose_name_plural = "Entradas de blog"
