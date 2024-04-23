from rest_framework import viewsets
from apirest.permissions import IsAdminOrCreateOnly
from rest_framework.parsers import MultiPartParser, JSONParser
from .serializers import FormSubmissionSerializer
from wagtail.contrib.forms.models import FormSubmission
from wagtail.api.v2.views import PagesAPIViewSet


class FormSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = FormSubmissionSerializer
    queryset = FormSubmission.objects.all()
    permission_classes = [IsAdminOrCreateOnly]
    parser_classes = [MultiPartParser, JSONParser]


class PaginasAPIViewSet(PagesAPIViewSet):
    detail_only_fields = []
    listing_default_fields = PagesAPIViewSet.listing_default_fields + [
        'title',
        'slug',
        'first_published_at',
        'parent',
        'site',
        'icono',
        'color',
    ]


class NoticiasAPIViewSet(PagesAPIViewSet):
    listing_default_fields = PagesAPIViewSet.listing_default_fields + [
        'categoria',
    ]


class EventosAPIViewSet(PagesAPIViewSet):
    listing_default_fields = PagesAPIViewSet.listing_default_fields + [
        'categoria',
    ]


class AvisosAPIViewSet(PagesAPIViewSet):
    listing_default_fields = PagesAPIViewSet.listing_default_fields + [
        'categoria',
    ]


class LugaresAPIViewSet(PagesAPIViewSet):
    """API Viewset para mostrar la categoría para páginas de tipo lugar."""
    listing_default_fields = PagesAPIViewSet.listing_default_fields + [
        'categoria',
    ]
