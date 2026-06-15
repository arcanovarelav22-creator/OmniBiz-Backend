from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500, blank=True, default='')
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    stock_quantity = models.IntegerField(default=0)
    is_critical = models.BooleanField(default=False)

    def __str__(self):
        return self.name