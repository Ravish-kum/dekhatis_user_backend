from django.contrib import admin
from django.urls import path, include

from . import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('backend.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'utils.views.error_404'
handler500 = 'utils.views.error_500'
