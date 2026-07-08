from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .models import Product, Client, Sale, SaleItem, RouteVisit # 🎯 NUEVO: Importamos el modelo de visitas
from .serializers import ProductSerializer, ClientSerializer, RouteVisitSerializer # 🎯 NUEVO: Importamos el serializador de visitas
from datetime import date

# ==========================================
# 📦 MÓDULO DE PRODUCTOS (INVENTARIO)
# ==========================================
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


# ==========================================
# 🤝 MÓDULO DE CLIENTES
# ==========================================
class ClientListCreateAPIView(generics.ListCreateAPIView):
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer

class ClientRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'pk'


# ==========================================
# 💸 MÓDULO DE VENTAS (MANUAL Y ATÓMICO)
# ==========================================
class SaleCreateAPIView(APIView):
    def post(self, request):
        data = request.data
        print("Datos de venta recibidos en Django:", data)
        
        try:
            with transaction.atomic():
                client_id = data.get('client')
                total_amount = data.get('total_amount')
                
                if not client_id or not total_amount:
                    return Response({"error": "Faltan campos obligatorios: client o total_amount"}, status=status.HTTP_400_BAD_REQUEST)
                
                client_obj = Client.objects.get(id=int(client_id))
                
                # Crear venta cabecera
                sale = Sale.objects.create(
                    client=client_obj,
                    payment_type=data.get('payment_type', 'CASH'),
                    total_amount=float(total_amount)
                )
                
                # Procesar carrito
                items_data = data.get('items', [])
                for item in items_data:
                    product_id = item.get('product')
                    product_obj = Product.objects.get(id=int(product_id))
                    
                    quantity = int(item.get('quantity', 1))
                    price_per_unit = float(item.get('price_per_unit', 0.00))
                    
                    SaleItem.objects.create(
                        sale=sale,
                        product=product_obj,
                        quantity=quantity,
                        price_per_unit=price_per_unit
                    )
                    
                    # Descontar stock
                    product_obj.stock_quantity -= quantity
                    product_obj.save()
                    
            return Response({"message": "Venta guardada con éxito", "sale_id": sale.id}, status=status.HTTP_201_CREATED)
            
        except Client.DoesNotExist:
            return Response({"error": f"El cliente con ID {client_id} no existe."}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Uno de los productos en el carrito no existe."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Fallo interno: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


# ==========================================
# 🗺️ MÓDULO CRM (RUTAS DIARIAS DE VISITAS)
# ==========================================

class DailyRouteListView(generics.ListAPIView):
    """
    🎯 Lógica: Filtra y retorna únicamente la secuencia de visitas programadas 
    para la fecha de hoy, manteniendo sincronizado el checklist del Moto G55.
    """
    serializer_class = RouteVisitSerializer

    def get_queryset(self):
        # Filtra las visitas planificadas para el día de hoy
        return RouteVisit.objects.filter(planned_date=date.today()).order_by('sequence_order')


class RouteVisitUpdateStatusAPIView(APIView):
    """
    🎯 Lógica: Recibe los cambios en caliente desde la calle (VISITED / NO_SALE)
    y actualiza los estados y comentarios correspondientes en la base de datos de Render.
    """
    def patch(self, request, pk):
        try:
            visit = RouteVisit.objects.get(pk=pk)
            data = request.data
            
            # Actualizamos los campos enviados por la app en Flutter
            if 'status' in data:
                visit.status = data['status']
            if 'notes' in data:
                visit.notes = data['notes']
            if 'start_time' in data and data['start_time']:
                visit.start_time = data['start_time']
            if 'end_time' in data and data['end_time']:
                visit.end_time = data['end_time']
                
            visit.save()
            return Response({"message": "Estado de visita actualizado correctamente"}, status=status.HTTP_200_OK)
            
        except RouteVisit.DoesNotExist:
            return Response({"error": "La visita especificada no existe."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error al actualizar la visita: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)