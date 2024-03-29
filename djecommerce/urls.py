from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls', namespace='core')),
    path('', include('sellers.urls', namespace='sellers')),
    path('sw.js', TemplateView.as_view(template_name="sw.js", content_type='text/javascript'))
]

handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'
handler413 = 'core.views.error_413'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)