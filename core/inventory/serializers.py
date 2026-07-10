from rest_framework import serializers
from .models import Product, Client, Sale, SaleItem, RouteVisit 

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'image_url', 'price_per_unit', 'stock_quantity', 'is_critical']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        # 🎯 CORREGIDO: Únicamente los campos reales que existen en el modelo de base de datos
        fields = ['id', 'name', 'owner_name', 'phone', 'address', 'status', 'created_at']

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'price_per_unit']

class SaleCreateSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'client', 'payment_type', 'total_amount', 'items']


# ==========================================
# 🗺️ MÓDULO CRM / SERIALIZADOR DE RUTAS
# ==========================================
class RouteVisitSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(source='client.id', read_only=True)

    class Meta:
        model = RouteVisit
        fields = [
            'id', 
            'client_id', 
            'client_name', 
            'status', 
            'notes', 
            'planned_date', 
            'sequence_order', 
            'start_time', 
            'end_time'
        ]