from django.urls import path
from .views import (
    ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView,
    ClientListCreateAPIView, ClientRetrieveUpdateDestroyAPIView,
    SaleCreateAPIView  # 👈 La vista transaccional que creamos
) 

urlpatterns = [
    # 📦 MÓDULO DE PRODUCTOS (INVENTARIO)
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    
    # 🤝 MÓDULO DE CLIENTES & SEMÁFORO FINTECH
    path('clients/', ClientListCreateAPIView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroyAPIView.as_view(), name='client-detail'),
    
    # 💸 MÓDULO DE VENTAS (EL ENDPOINT QUE NECESITA TU POS)
    path('sales/', SaleCreateAPIView.as_view(), name='sale-create'),
]