from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
import json
from .models import Product, Client, Sale, SaleItem

class SaleCreateAPIView(APIView):
    def post(self, request):
        data = request.POST # Recibimos como form-data
        try:
            with transaction.atomic():
                client = Client.objects.get(id=int(data['client']))
                sale = Sale.objects.create(
                    client=client,
                    payment_type=data.get('payment_type', 'CASH'),
                    total_amount=float(data['total_amount'])
                )
                
                # Los items vienen como un string JSON que debemos decodificar
                items = json.loads(data['items'])
                for item in items:
                    prod = Product.objects.get(id=int(item['product']))
                    SaleItem.objects.create(
                        sale=sale,
                        product=prod,
                        quantity=int(item['quantity']),
                        price_per_unit=float(item['price_per_unit'])
                    )
                    prod.stock_quantity -= int(item['quantity'])
                    prod.save()
                    
            return Response({"message": "Éxito"}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)