from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 🔐 Panel de Administración de Django
    path('admin/', admin.site.urls),
    
    # 📦 Enrutador unificado para tu módulo de Inventario, Clientes y Ventas
    path('inventory/', include('inventory.urls')), 
]