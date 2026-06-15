from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'image_url', 'price_per_unit', 'stock_quantity', 'is_critical']