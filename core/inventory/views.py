from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .models import Product, Client, Sale, SaleItem

class SaleCreateAPIView(APIView):
    def post(self, request):
        data = request.data
        # Debug: Imprimimos lo que recibe Django
        print("Datos recibidos en Django:", data) 
        
        try:
            with transaction.atomic():
                # 1. Validaciones básicas
                client_id = data.get('client')
                total_amount = data.get('total_amount')
                
                if not client_id or not total_amount:
                    return Response({"error": "Faltan campos obligatorios: client o total_amount"}, status=400)
                
                client = Client.objects.get(id=int(client_id))
                
                # 2. Crear Venta
                sale = Sale.objects.create(
                    client=client,
                    payment_type=data.get('payment_type', 'CASH'),
                    total_amount=float(total_amount)
                )
                
                # 3. Procesar Items
                items = data.get('items', [])
                for item in items:
                    prod = Product.objects.get(id=int(item['product']))
                    SaleItem.objects.create(
                        sale=sale,
                        product=prod,
                        quantity=int(item['quantity']),
                        price_per_unit=float(item['price_per_unit'])
                    )
                    # Descontar stock
                    prod.stock_quantity -= int(item['quantity'])
                    prod.save()
                    
            return Response({"message": "Éxito"}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)