from rest_framework import serializers
from .models import Product, Client  # Importación unificada de ambos modelos

# ==========================================
# 📦 SERIALIZADOR DE PRODUCTOS
# ==========================================
class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'image_url', 'price_per_unit', 'stock_quantity', 'is_critical']


# ==========================================
# 🤝 SERIALIZADOR DE CLIENTES
# ==========================================
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id', 
            'name', 
            'owner_name', 
            'phone', 
            'address', 
            'credit_limit', 
            'current_balance', 
            'status', 
            'created_at'
        ]