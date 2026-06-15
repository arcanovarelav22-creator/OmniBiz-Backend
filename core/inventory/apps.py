import os
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'

    def ready(self):
        # Conectamos una función para que se ejecute JUSTO DESPUÉS de las migraciones
        post_migrate.connect(create_custom_superuser, sender=self)

def create_custom_superuser(sender, **kwargs):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # 🎯 Define aquí las credenciales de tu administrador para la nube
    username = 'admin'
    email = 'admin@omnibiz.com'
    password = 'TuContrasenaSegura123'  # <-- Cambia esto por la contraseña que quieras
    
    if not User.objects.filter(username=username).exists():
        print("🚀 Creando superusuario automático en PostgreSQL...")
        User.objects.create_superuser(username=username, email=email, password=password)
        print("✅ Superusuario creado con éxito.")
    else:
        print("ℹ️ El superusuario ya existe en la base de datos.")