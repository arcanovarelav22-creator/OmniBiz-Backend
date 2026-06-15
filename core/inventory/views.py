from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

# Esta vista se encarga de LISTAR (GET) y CREAR (POST) productos
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer