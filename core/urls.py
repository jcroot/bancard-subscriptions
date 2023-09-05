from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import renderers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.schemas import get_schema_view

from core import settings, api_urls

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('gettoken/', obtain_auth_token, name='api_token_auth'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += api_urls.urlpatterns

urlpatterns += [
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema-yaml'},
    ), name='swagger-ui'),
    path('openapi.yaml', get_schema_view(
        title="Bancard subscriptions API",
        renderer_classes=[renderers.OpenAPIRenderer]
    ), name='openapi-schema-yaml'),
    path('openapi.json', get_schema_view(
        title="Bancard subscriptions API",
        renderer_classes = [renderers.JSONOpenAPIRenderer],
    ), name='openapi-schema-json'),
]
