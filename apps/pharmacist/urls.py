from django.urls import path
from apps.pharmacist.views import (
    MedicineListCreateView, MedicineDetailView, MedicineDeactivateView,
    InventoryListCreateView, InventoryMedicineDetailView, InventoryStockUpdateView, InventoryFlagLowView, InventoryDispenseView
)

urlpatterns = [
    # Medicine routes
    path('medicines', MedicineListCreateView.as_view(), name='medicine-list-create'),
    path('medicines/<int:medicineId>', MedicineDetailView.as_view(), name='medicine-detail'),
    path('medicines/<int:medicineId>/deactivate', MedicineDeactivateView.as_view(), name='medicine-deactivate'),

    # Inventory routes
    path('inventory/medicine', InventoryListCreateView.as_view(), name='inventory-list-create'),
    path('inventory/medicine/<int:medicineId>', InventoryMedicineDetailView.as_view(), name='inventory-medicine-detail'),
    path('inventory/medicine/stock/<int:medicineStockId>', InventoryStockUpdateView.as_view(), name='inventory-stock-update'),
    path('inventory/medicine/stock/<int:medicineStockId>/flag-low', InventoryFlagLowView.as_view(), name='inventory-flag-low'),
    path('inventory/medicine/dispense', InventoryDispenseView.as_view(), name='inventory-dispense'),
]
