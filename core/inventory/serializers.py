from rest_framework import serializers
from .models import Product, Client, Sale, SaleItem

# ==========================================
# 📦 MÓDULO DE PRODUCTOS
# ==========================================
class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'image_url', 'price_per_unit', 'stock_quantity', 'is_critical']


# ==========================================
# 🤝 MÓDULO DE CLIENTES
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


# ==========================================
# 💸 MÓDULO DE VENTAS / TRANSACCIONES
# ==========================================
class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'price_per_unit']


class SaleCreateSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'client', 'payment_type', 'total_amount', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        client = validated_data.get('client')
        payment_type = validated_data.get('payment_type', 'CASH')
        total_amount = validated_data.get('total_amount', 0.00)
        
        sale = Sale.objects.create(
            client=client,
            payment_type=payment_type,
            total_amount=total_amount
        )
        
        for item_data in items_data:
            SaleItem.objects.create(sale=sale, **item_data)
            
            product = item_data['product']
            product.stock_quantity -= item_data['quantity']
            product.save()
            
        if sale.payment_type == 'CREDIT':
            client = sale.client
            client.current_balance += sale.total_amount
            client.save()
            
        return sale