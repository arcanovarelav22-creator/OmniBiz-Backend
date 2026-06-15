from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    is_critical = models.BooleanField(default=False)
    # Almacena de manera correcta el archivo físico en el directorio /media/products/
    image_url = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name