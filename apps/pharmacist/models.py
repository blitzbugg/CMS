from django.db import models

class TblMedicine(models.Model):
    MedicineId = models.AutoField(primary_key=True)
    MedicineName = models.CharField(max_length=255)
    Category = models.CharField(max_length=100)
    ManufacturingDate = models.DateField()
    ExpiryDate = models.DateField()
    Unit = models.CharField(max_length=50)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.MedicineName


class TblMedicineStock(models.Model):
    MedicineStockId = models.AutoField(primary_key=True)
    MedicineId = models.ForeignKey(TblMedicine, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    IsLowStock = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.MedicineId.MedicineName} - {self.Quantity} in stock"
