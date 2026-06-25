from django.urls import path
from .views import (
    ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView,
    ClientListCreateAPIView, ClientRetrieveUpdateDestroyAPIView,
    SaleCreateAPIView  # Importación de la nueva vista
) 

urlpatterns = [
    # 📦 MÓDULO DE PRODUCTOS (INVENTARIO)
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    
    # 🤝 MÓDULO DE CLIENTES & SEMÁFORO
    path('clients/', ClientListCreateAPIView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroyAPIView.as_view(), name='client-detail'),
    
    # 💸 MÓDULO DE VENTAS (NUEVO)
    path('sales/', SaleCreateAPIView.as_view(), name='sale-create'),
]