from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.pharmacist.models import TblMedicine, TblMedicineStock
from apps.pharmacist.serializers import TblMedicineSerializer, TblMedicineStockSerializer

# Medicine Views
class MedicineListCreateView(APIView):
    def get(self, request):
        queryset = TblMedicine.objects.filter(IsActive=True)
        serializer = TblMedicineSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TblMedicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MedicineDetailView(APIView):
    def get(self, request, medicineId):
        medicine = get_object_or_404(TblMedicine, MedicineId=medicineId)
        serializer = TblMedicineSerializer(medicine)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, medicineId):
        medicine = get_object_or_404(TblMedicine, MedicineId=medicineId)
        serializer = TblMedicineSerializer(medicine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MedicineDeactivateView(APIView):
    def patch(self, request, medicineId):
        medicine = get_object_or_404(TblMedicine, MedicineId=medicineId)
        medicine.IsActive = False
        medicine.save()
        return Response({"message": "Medicine deactivated successfully"}, status=status.HTTP_200_OK)


# Inventory Views
class InventoryListCreateView(APIView):
    def get(self, request):
        queryset = TblMedicineStock.objects.all()
        serializer = TblMedicineStockSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Prevent creating multiple stock rows for same medicine
        medicine_id = request.data.get('MedicineId')
        if TblMedicineStock.objects.filter(MedicineId=medicine_id).exists():
            return Response({"error": "Inventory stock already exists for this medicine"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TblMedicineStockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class InventoryMedicineDetailView(APIView):
    def get(self, request, medicineId):
        stock = get_object_or_404(TblMedicineStock, MedicineId=medicineId)
        serializer = TblMedicineStockSerializer(stock)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InventoryStockUpdateView(APIView):
    def put(self, request, medicineStockId):
        stock = get_object_or_404(TblMedicineStock, MedicineStockId=medicineStockId)
        serializer = TblMedicineStockSerializer(stock, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class InventoryFlagLowView(APIView):
    def patch(self, request, medicineStockId):
        stock = get_object_or_404(TblMedicineStock, MedicineStockId=medicineStockId)
        stock.IsLowStock = True
        stock.save()
        return Response({"message": "Medicine flagged as low stock"}, status=status.HTTP_200_OK)


class InventoryDispenseView(APIView):
    def post(self, request):
        medicine_id = request.data.get('medicineId')
        quantity = request.data.get('quantity')

        if not medicine_id or quantity is None:
            return Response({"error": "Both medicineId and quantity are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response({"error": "Quantity must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Quantity must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        stock = get_object_or_404(TblMedicineStock, MedicineId=medicine_id)
        if stock.Quantity < quantity:
            return Response({"error": f"Insufficient stock. Available: {stock.Quantity}"}, status=status.HTTP_400_BAD_REQUEST)

        # Subtract quantity from inventory stock
        stock.Quantity -= quantity
        # Auto-flag as low stock if quantity drops below 10
        if stock.Quantity < 10:
            stock.IsLowStock = True
        stock.save()

        return Response({
            "message": "Medicine dispensed successfully",
            "medicineId": medicine_id,
            "dispensedQuantity": quantity,
            "remainingQuantity": stock.Quantity,
            "isLowStock": stock.IsLowStock
        }, status=status.HTTP_200_OK)
