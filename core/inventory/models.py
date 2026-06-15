from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price_per_unit = models.DecimalField(max_length=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    is_critical = models.BooleanField(default=False)
    
    # 🎯 CAMBIA O AGREGA ESTA LÍNEA:
    # upload_to indica la carpeta interna o el prefijo donde se organizarán las fotos
    image_url = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name