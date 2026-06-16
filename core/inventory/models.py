from django.db import models

class Product(models.Model):
    # 🎯 NUEVO: Código SKU único para control de inventario
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    is_critical = models.BooleanField(default=False)
    image_url = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return f"{self.sku} - {self.name}" if self.sku else self.name