from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from search import views as search_views
from wtbase.urls import wagtailapi_router
from django.views.generic import TemplateView
from django.http import HttpResponse
import os
import redis

urlpatterns = [
    path("dadmin/", admin.site.urls),
    path("wadmin/", include(wagtailadmin_urls)),
    path("search/", search_views.search, name="search"),
    path('rest/v1/auth/', include('rest_framework.urls'), name='rest_framework'),
    path("rest/v1/", include('wtbase.urls'), name='wtbase'),
    path("rest/v1/", include('sanamente.urls'), name='sanamente'),
    path("rest/v1/", wagtailapi_router.urls, name='wagtailapi_router'),
]

if os.getenv("DJANGO_SETTINGS_MODULE").split('.')[-1] in ["production", "stagging"]:
    urlpatterns += [
        path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
             name='robots.txt'),
        # path('dadmin/defender/', include('gdmty_django_defender.urls')),
    ]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]