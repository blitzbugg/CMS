from django.urls import path
from apps.doctor.views import (
    ConsultationCreateView, ConsultationPatientListView, ConsultationDoctorListView, ConsultationAppointmentDetailView,
    MedicinePrescriptionCreateView, MedicinePrescriptionDetailView, MedicinePrescriptionAppointmentListView, MedicinePrescriptionPatientListView, MedicinePrescriptionDoctorListView,
    LabTestPrescriptionCreateView, LabTestPrescriptionDetailView, LabTestPrescriptionAppointmentListView, LabTestPrescriptionPatientListView
)

urlpatterns = [
    # Consultation routes
    path('consultations', ConsultationCreateView.as_view(), name='consultation-create'),
    path('consultations/patient/<int:patientId>', ConsultationPatientListView.as_view(), name='consultation-patient-list'),
    path('consultations/doctor/<int:doctorId>', ConsultationDoctorListView.as_view(), name='consultation-doctor-list'),
    path('consultations/history/appointment/<int:appointmentId>', ConsultationAppointmentDetailView.as_view(), name='consultation-appointment-detail'),

    # Medicine Prescription routes
    path('prescriptions/medicine', MedicinePrescriptionCreateView.as_view(), name='prescription-medicine-create'),
    path('prescriptions/medicine/<int:prescriptionId>', MedicinePrescriptionDetailView.as_view(), name='prescription-medicine-detail'),
    path('prescriptions/medicine/appointment/<int:appointmentId>', MedicinePrescriptionAppointmentListView.as_view(), name='prescription-medicine-appointment-list'),
    path('prescriptions/medicine/patient/<int:patientId>', MedicinePrescriptionPatientListView.as_view(), name='prescription-medicine-patient-list'),
    path('prescriptions/medicine/history/patient/<int:patientId>', MedicinePrescriptionPatientListView.as_view(), name='prescription-medicine-patient-history'),
    path('prescriptions/medicine/history/doctor/<int:doctorId>', MedicinePrescriptionDoctorListView.as_view(), name='prescription-medicine-doctor-history'),

    # Lab Test Prescription routes
    path('prescriptions/labtest', LabTestPrescriptionCreateView.as_view(), name='prescription-labtest-create'),
    path('prescriptions/labtest/<int:prescriptionId>', LabTestPrescriptionDetailView.as_view(), name='prescription-labtest-detail'),
    path('prescriptions/labtest/appointment/<int:appointmentId>', LabTestPrescriptionAppointmentListView.as_view(), name='prescription-labtest-appointment-list'),
    path('prescriptions/labtest/patient/<int:patientId>', LabTestPrescriptionPatientListView.as_view(), name='prescription-labtest-patient-list'),
]
