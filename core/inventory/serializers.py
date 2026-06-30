from rest_framework import serializers
from .models import Product, Client, Sale, SaleItem

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'image_url', 'price_per_unit', 'stock_quantity', 'is_critical']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'owner_name', 'phone', 'address', 'credit_limit', 'current_balance', 'status', 'created_at']

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'price_per_unit']

class SaleCreateSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'client', 'payment_type', 'total_amount', 'items']