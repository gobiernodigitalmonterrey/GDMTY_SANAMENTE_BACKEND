from rest_framework.fields import CharField, Field
from wagtail.rich_text import expand_db_html
from threadlocals.threadlocals import get_current_request
from pyproj import Transformer
from django.conf import settings

# Create your serializers here.


def get_rendition_attrs(rendition):
    attrs_dict = dict(rendition.attrs_dict)
    if settings.DEVMODE:
        if settings.DEFAULT_FILE_STORAGE != 'storages.backends.gcloud.GoogleCloudStorage':
            attrs_dict['src'] = settings.WAGTAILADMIN_BASE_URL + attrs_dict['src']
    return attrs_dict


class ImagenLgSerializer(Field):

    def to_internal_value(self, data):
        if isinstance(data, bool) or not isinstance(data, (str, int, float,)):
            self.fail('invalid')
        value = str(data).strip()
        return value

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "title": instance.title,
            "meta": {
                "type": "wagtailimages.Image",
                'background': get_rendition_attrs(instance.get_rendition('fill-1920x1080')),
                'hero': get_rendition_attrs(instance.get_rendition('fill-1280x720')),
                'header': get_rendition_attrs(instance.get_rendition('fill-1600x300')),
                'blog-lg': get_rendition_attrs(instance.get_rendition('fill-1200x600')),
                'blog-md': get_rendition_attrs(instance.get_rendition('fill-900x585')),
            }
        }
        return representation


class ImagenMdSerializer(Field):

    def to_internal_value(self, data):
        if isinstance(data, bool) or not isinstance(data, (str, int, float,)):
            self.fail('invalid')
        value = str(data).strip()
        return value

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "title": instance.title,
            "meta": {
                "type": "wagtailimages.Image",
                'blog-lg': get_rendition_attrs(instance.get_rendition('fill-1200x600')),
                'blog-md': get_rendition_attrs(instance.get_rendition('fill-900x585')),
                'blog-sm': get_rendition_attrs(instance.get_rendition('fill-600x390')),
                'blog-xs': get_rendition_attrs(instance.get_rendition('fill-400x260')),
            }
        }
        return representation


class ImagenSmSerializer(Field):

        def to_internal_value(self, data):
            if isinstance(data, bool) or not isinstance(data, (str, int, float,)):
                self.fail('invalid')
            value = str(data).strip()
            return value

        def to_representation(self, instance):
            representation = {
                "id": instance.id,
                "title": instance.title,
                "meta": {
                    "type": "wagtailimages.Image",
                    'blog-md': get_rendition_attrs(instance.get_rendition('fill-900x585')),
                    'blog-sm': get_rendition_attrs(instance.get_rendition('fill-600x390')),
                    'blog-xs': get_rendition_attrs(instance.get_rendition('fill-400x260')),
                    'thumbnail': get_rendition_attrs(instance.get_rendition('fill-250x250')),
                }
            }
            return representation


class ImagenXsSerializer(Field):

            def to_internal_value(self, data):
                if isinstance(data, bool) or not isinstance(data, (str, int, float,)):
                    self.fail('invalid')
                value = str(data).strip()
                return value

            def to_representation(self, instance):
                representation = {
                    "id": instance.id,
                    "title": instance.title,
                    "meta": {
                        "type": "wagtailimages.Image",
                        'blog-xs': get_rendition_attrs(instance.get_rendition('fill-400x260')),
                        'thumbnail': get_rendition_attrs(instance.get_rendition('fill-250x250')),
                        'logo-rect': get_rendition_attrs(instance.get_rendition('fill-250x100')),
                        'logo-quad': get_rendition_attrs(instance.get_rendition('fill-100x100')),
                        'icon': get_rendition_attrs(instance.get_rendition('fill-40x40')),
                    }
                }
                return representation


class ImagenFotografia(Field):

    def to_internal_value(self, data):
        if isinstance(data, bool) or not isinstance(data, (str, int, float,)):
            self.fail('invalid')
        value = str(data).strip()
        return value

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "title": instance.title,
            "meta": {
                "type": "wagtailimages.Image",
                'fotografia-port-md': get_rendition_attrs(instance.get_rendition('fill-585x900')),
                'fotografia-port-sm': get_rendition_attrs(instance.get_rendition('fill-390x600')),
                'fotografia-port-xs': get_rendition_attrs(instance.get_rendition('fill-260x400')),
                'fotografia-quad-md': get_rendition_attrs(instance.get_rendition('fill-900x900')),
                'fotografia-quad-sm': get_rendition_attrs(instance.get_rendition('fill-600x600')),
                'fotografia-quad-xs': get_rendition_attrs(instance.get_rendition('fill-400x400')),
                'thumbnail': get_rendition_attrs(instance.get_rendition('fill-250x250')),
            }
        }
        return representation


class CharFieldNombreSerializer(Field):

    def to_representation(self, instance):
        return {"pk": instance.pk, "nombre": instance.nombre}


class AutorBioSerializer(Field):

    def to_representation(self, instance):
        # print(instance.avatar.get_rendition('fill-300x300'))
        return {
            "pk": instance.pk,
            "nombre": instance.nombre,
            "biografia_autor": instance.biografia_autor,
            "avatar": get_rendition_attrs(instance.avatar.get_rendition('fill-300x300')) if instance.avatar else None
        }


class RichTextSerializer(CharField):

    def to_representation(self, instance):
        to_representation = super().to_representation(instance)
        representation = expand_db_html(to_representation)
        request = get_current_request()
        root_url = f"{request.scheme}://{request.get_host()}"
        representation = representation.replace('src="/', f'src="{root_url}/').replace('\n', '') \
            .replace('href="/', f'href="{root_url}/') \
            .replace('<div>    <iframe', '<div class=\"custom-embed\"><iframe')
        return representation


class Geom3857to4326Serializer(Field):

    def to_representation(self, instance):
        return {
            'coords': Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True).transform(instance[0], instance[1])
        }
