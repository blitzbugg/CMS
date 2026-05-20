from django.urls import path
from apps.lab_technician.views import (
    LabTestListCreateView, LabTestDetailView, LabTestDeactivateView,
    LabTestResultAppointmentView, LabTestResultListView, LabTestResultRecordView, LabTestPrescriptionDeactivateView
)

urlpatterns = [
    # Lab Test routes
    path('labtests', LabTestListCreateView.as_view(), name='labtest-list-create'),
    path('labtests/<int:labTestId>', LabTestDetailView.as_view(), name='labtest-detail'),
    path('labtests/<int:labTestId>/deactivate', LabTestDeactivateView.as_view(), name='labtest-deactivate'),

    # Lab Results routes
    path('labtests/results/appointment/<int:appointmentId>', LabTestResultAppointmentView.as_view(), name='labtest-results-appointment'),
    path('labtests/results', LabTestResultListView.as_view(), name='labtest-results-list'),
    path('labtests/results/<int:labTestPrescriptionId>', LabTestResultRecordView.as_view(), name='labtest-result-record'),
    path('labtests/<int:labTestPrescriptionId>/deactivate', LabTestPrescriptionDeactivateView.as_view(), name='labtest-prescription-deactivate'),
]
