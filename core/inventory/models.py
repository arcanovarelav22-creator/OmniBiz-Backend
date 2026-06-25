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
    phone = models.CharField(max_length=20, verbose_name="Teléfono de Contacto")
    address = models.TextField(verbose_name="Dirección Completa / Ruta de Entrega")
    
    # Fintech Core: Control Financiero de Crédito
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Límite de Crédito")
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Saldo Pendiente")
    
    # Control Automatizado del Semáforo
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
# 💸 MÓDULO DE VENTAS (NUEVO)
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
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Venta #{self.sale.id})"