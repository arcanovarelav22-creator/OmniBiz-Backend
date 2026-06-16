from django.urls import path
from .views import ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView 

urlpatterns = [
    # Endpoint para listar y crear productos (POST y GET)
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    
    # Endpoint para ver, editar y eliminar un producto por su ID (GET, PUT, DELETE)
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
]