from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'stock_quantity', 'price_per_unit', 'is_critical')
    list_filter = ('is_critical',)
    search_fields = ('name',)