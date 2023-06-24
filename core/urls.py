from django.contrib import admin
from django.urls import path, include
from .settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static
from .yasg import urlpatterns as doc_urls

urlpatterns = [
                  # Django Admin Site
                  path('admin/', admin.site.urls),
                  # Account Endpoints
                  path('api/', include('core.apps.accounts.urls')),
                  path('api/', include('core.apps.projects.urls')),
                  path('api-auth/', include('rest_framework.urls')),
              ] + static(MEDIA_URL, document_root=MEDIA_ROOT)

# Добавляем URL для нашей API документации
urlpatterns += doc_urls
