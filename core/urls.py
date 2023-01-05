from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core import settings, api_urls

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += api_urls.urlpatterns
