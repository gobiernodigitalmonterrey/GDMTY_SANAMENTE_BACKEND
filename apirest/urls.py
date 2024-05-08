from rest_framework import routers
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

urlpatterns = []

drf_router = routers.DefaultRouter()
wagtailapi_router = WagtailAPIRouter('wagtailapi')

wagtailapi_router.register_endpoint(r'imagenes', ImagesAPIViewSet)
wagtailapi_router.register_endpoint(r'documentos', DocumentsAPIViewSet)
