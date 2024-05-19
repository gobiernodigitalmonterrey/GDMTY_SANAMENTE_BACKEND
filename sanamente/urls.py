from wtbase.urls import drf_router
from .viewsets import (SanamenteAPIViewSet, CategoriaActividadBienestarViewSet, CategoriaServicioProfesionalViewSet,
                       EspecialidadServicioProfesionalViewSet, CategoriaEntradaBlogViewSet)
from wtbase.urls import wagtailapi_router

#

urlpatterns = []

wagtailapi_router.register_endpoint(r'paginas', SanamenteAPIViewSet)
drf_router.register(r'sanamente/categoria-actividad-bienestar', CategoriaActividadBienestarViewSet, basename='sanamente-categoria-actividad-bienestar')
drf_router.register(r'sanamente/categoria-servicio-profesional', CategoriaServicioProfesionalViewSet, basename='sanamente-categoria-servicio-profesional')
drf_router.register(r'sanamente/categoria-entrada-blog', CategoriaEntradaBlogViewSet, basename='sanamente-categoria-entrada-blog')
drf_router.register(r'sanamente/especialidad-servicio-profesional', EspecialidadServicioProfesionalViewSet, basename='especialidad-servicio-profesional')

urlpatterns += drf_router.urls
