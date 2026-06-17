from rest_framework import generics
from .models import Product, Client
from .serializers import ProductSerializer, ClientSerializer

# ==========================================
# 📦 VISTAS DEL MÓDULO DE PRODUCTOS
# ==========================================
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


# ==========================================
# 🤝 VISTAS DEL MÓDULO DE CLIENTES
# ==========================================
class ClientListCreateAPIView(generics.ListCreateAPIView):
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer

class ClientRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'pk'