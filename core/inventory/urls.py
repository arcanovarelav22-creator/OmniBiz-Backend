from django.urls import path
from .views import (
    ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView,
    ClientListCreateAPIView, ClientRetrieveUpdateDestroyAPIView,
    SaleCreateAPIView,
    DailyRouteListView, RouteVisitUpdateStatusAPIView
) 

urlpatterns = [
    # === Módulo de Inventario (Productos) ===
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    
    # === Módulo de Cobranza (Clientes) ===
    path('clients/', ClientListCreateAPIView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroyAPIView.as_view(), name='client-detail'),
    
    # === Módulo de Ventas (Facturación / POS) ===
    path('sales/', SaleCreateAPIView.as_view(), name='sale-create'),

    # === 🗺️ MÓDULO CRM / RUTAS DIARIAS (Conexión para la App) ===
    path('routes/daily/', DailyRouteListView.as_view(), name='daily-route-list'),
    path('routes/<int:pk>/update_status/', RouteVisitUpdateStatusAPIView.as_view(), name='route-visit-update-status'),
]