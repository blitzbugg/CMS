from rest_framework import serializers
from apps.pharmacist.models import TblMedicine, TblMedicineStock

class TblMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblMedicine
        fields = '__all__'

    def validate(self, data):
        # Validation Requirement: ExpiryDate must be after ManufacturingDate
        mfg = data.get('ManufacturingDate')
        exp = data.get('ExpiryDate')
        if mfg and exp and exp <= mfg:
            raise serializers.ValidationError({"ExpiryDate": "ExpiryDate must be after ManufacturingDate."})
        return data


class TblMedicineStockSerializer(serializers.ModelSerializer):
    MedicineName = serializers.CharField(source='MedicineId.MedicineName', read_only=True)

    class Meta:
        model = TblMedicineStock
        fields = ['MedicineStockId', 'MedicineId', 'MedicineName', 'Quantity', 'IsLowStock']
