from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    # 🎯 LA SOLUCIÓN: Sobrescribimos el campo para que acepte archivos binarios en el POST
    # y devuelva la URL completa en el GET de forma automática.
    image_url = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'image_url', 'price_per_unit', 'stock_quantity', 'is_critical']