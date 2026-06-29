from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .models import Product, Client, Sale, SaleItem
from .serializers import ProductSerializer, ClientSerializer

# ==========================================
# 📦 VISTAS DEL MÓDULO DE PRODUCTOS
# ==========================================
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


# ==========================================
# 🤝 VISTAS DEL MÓDULO DE CLIENTES
# ==========================================
class ClientListCreateAPIView(generics.ListCreateAPIView):
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer

class ClientRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'pk'


# ==========================================
# 💸 VISTAS DEL MÓDULO DE VENTAS (MANUAL Y BLINDADO)
# ==========================================
class SaleCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            
            # Usamos una transacción atómica: si algo falla, no se guarda nada a medias
            with transaction.atomic():
                
                # 1. Extraer los datos exactos que envía Flutter
                client_id = data.get('client')
                client_obj = Client.objects.get(id=client_id)
                
                payment_type = data.get('payment_type', 'CASH')
                total_amount = data.get('total_amount', 0.00)
                
                # Crear la cabecera de la Venta
                sale = Sale.objects.create(
                    client=client_obj,
                    payment_type=payment_type,
                    total_amount=total_amount
                )
                
                # 2. Procesar los productos del carrito
                items_data = data.get('items', [])
                for item in items_data:
                    product_id = item.get('product')
                    product_obj = Product.objects.get(id=product_id)
                    
                    quantity = int(item.get('quantity', 1))
                    price_per_unit = float(item.get('price_per_unit', 0.00))
                    
                    # Guardar el producto en la nota de venta
                    SaleItem.objects.create(
                        sale=sale,
                        product=product_obj,
                        quantity=quantity,
                        price_per_unit=price_per_unit
                    )
                    
                    # ¡Magia! Descontamos el stock físico directamente aquí
                    product_obj.stock_quantity -= quantity
                    product_obj.save()
                    
                # 3. Si la venta es a crédito, sumar la deuda al saldo del cliente
                if payment_type == 'CREDIT':
                    client_obj.current_balance = float(client_obj.current_balance) + float(total_amount)
                    client_obj.save()
                    
            return Response({"mensaje": "Venta procesada con éxito", "id": sale.id}, status=status.HTTP_201_CREATED)
            
        except Client.DoesNotExist:
            return Response({"error": "El cliente no existe en la base de datos."}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Un producto del carrito no existe."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Fallo del servidor: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)