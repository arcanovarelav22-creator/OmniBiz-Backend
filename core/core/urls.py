from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 🎯 CORREGIDO: Ruta limpia y estándar para el panel de administración
    path('admin/', admin.site.urls), 
    
    # Ruta para la API de tu inventario
    path('api/v1/inventory/', include('inventory.urls')),
]

# Servir archivos multimedia (imágenes de productos) en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)