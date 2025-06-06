from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from media.views import home

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('media/', include('media.urls')),
    path('api/store/', include('store.urls')),
    path('pages/', include('pages.urls')),  # New URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)