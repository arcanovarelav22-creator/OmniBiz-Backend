from django.db import models

# ==========================================
# 📦 MÓDULO DE PRODUCTOS
# ==========================================
class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    is_critical = models.BooleanField(default=False)
    image_url = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return f"{self.sku} - {self.name}" if self.sku else self.name


# ==========================================
# 🤝 MÓDULO DE CLIENTES & SEMÁFORO FINTECH
# ==========================================
class Client(models.Model):
    STATUS_CHOICES = [
        ('EXCELLENT', 'Excelente (Al día)'),
        ('ALERT', 'Alerta de Stock (Próximo a agotarse)'),
        ('LATE', 'Moroso (Bloqueado)'),
    ]

    name = models.CharField(max_length=150, verbose_name="Nombre de la Tienda / Comercio")
    owner_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre del Encargado")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    address = models.TextField(verbose_name="Dirección Exacta")
    
    # Estado financiero adaptativo para el semáforo en Flutter
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='EXCELLENT', verbose_name="Estado de Cobranza")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-id']


# ==========================================
# 💸 MÓDULO DE VENTAS
# ==========================================
class Sale(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('CASH', 'Efectivo'),
        ('CREDIT', 'Crédito'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='sales')
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES, default='CASH')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta #{self.id} - {self.client.name}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} en Venta #{self.sale.id}"


# ==========================================
# 🗺️ MÓDULO CRM / CONTROL DE RUTAS DIARIAS (NUEVO)
# ==========================================
class RouteVisit(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('VISITED', 'VISITED'),
        ('NO_SALE', 'NO_SALE'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='route_visits')
    client_name = models.CharField(max_length=255)  # Nombre guardado en caché para optimizar la velocidad en la app
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True, null=True)
    planned_date = models.DateField(auto_now_add=True)  # Se asigna automáticamente al día actual al crearla
    sequence_order = models.IntegerField(default=0)  # Orden numérico en el checklist del Moto G55
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.client_name} - {self.status} ({self.planned_date})"

    class Meta:
        verbose_name = "Visita de Ruta"
        verbose_name_plural = "Visitas de Ruta"
        ordering = ['sequence_order']