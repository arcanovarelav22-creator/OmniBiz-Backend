from django.contrib import admin
from django.urls import path
from inventory.views import ProductListCreateAPIView

urlpatterns = [
    # 🎯 CORREGIDO: Ruta limpia y estándar para el Panel de Administración
    path('admin/', admin.site.urls),
    
    # Endpoint exacto acoplado al Data Source de tu App en Flutter
    path('api/v1/inventory/products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
]