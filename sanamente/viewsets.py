from wagtail.api.v2.views import PagesAPIViewSet
from .permissions import IsAdminOrReadOnly
from rest_framework import viewsets
from .serializers import CategoriaActividadBienestarSerializer,  CategoriaServicioProfesionalSerializer, CategoriaEntradaBlogSerializer
from .models import CategoriaActividadBienestar, CategoriaServicioProfesional, EspecialidadServicioProfesional, CategoriaEntradaBlog

# Add your viewsets here


class CategoriaActividadBienestarViewSet(viewsets.ModelViewSet):
    queryset = CategoriaActividadBienestar.objects.all()
    serializer_class = CategoriaActividadBienestarSerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoriaServicioProfesionalViewSet(viewsets.ModelViewSet):
    queryset = CategoriaServicioProfesional.objects.all()
    serializer_class = CategoriaServicioProfesionalSerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoriaEntradaBlogViewSet(viewsets.ModelViewSet):
    queryset = CategoriaEntradaBlog.objects.all()
    serializer_class = CategoriaEntradaBlogSerializer
    permission_classes = [IsAdminOrReadOnly]


class EspecialidadServicioProfesionalViewSet(viewsets.ModelViewSet):
    queryset = EspecialidadServicioProfesional.objects.all()
    serializer_class = CategoriaServicioProfesionalSerializer
    permission_classes = [IsAdminOrReadOnly]


class SanamenteAPIViewSet(PagesAPIViewSet):
    detail_only_fields = []
    listing_default_fields = PagesAPIViewSet.listing_default_fields + [
        'title',
        'slug',
        'first_published_at',
        'parent',
        'site',
        'categoria',
    ]
