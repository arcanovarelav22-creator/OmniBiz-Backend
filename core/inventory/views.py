from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

# 🎯 1. Vista para Listar (GET) y Crear (POST) productos
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer

# 🎯 2. Vista para Obtener (GET), Actualizar (PUT/PATCH) y Eliminar (DELETE) por ID
class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'  # Mapea directamente con el <int:pk> de tus URLs


from .models import Client
from .serializers import ClientSerializer

# 🎯 3. Vista para Listar (GET) y Registrar (POST) los clientes de Café Kiwa
class ClientListCreateAPIView(generics.ListCreateAPIView):
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer

# 🎯 4. Vista para Obtener (GET), Actualizar (PUT/PATCH) y Eliminar (DELETE) un cliente por ID
class ClientRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'pk'    