from django.urls import path
from apps.receptionist.views import (
    PatientListCreateView, PatientDetailView,
    AppointmentListCreateView, AppointmentPatientListView, AppointmentDoctorListView, AppointmentDetailView, AppointmentCancelView,
    BillingListCreateView, BillingDetailView
)

urlpatterns = [
    # Patient routes
    path('patients', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:patientId>', PatientDetailView.as_view(), name='patient-detail'),

    # Appointment routes
    path('appointments', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('appointments/patient/<int:patientId>', AppointmentPatientListView.as_view(), name='appointment-patient-list'),
    path('appointments/doctor/<int:doctorId>', AppointmentDoctorListView.as_view(), name='appointment-doctor-list'),
    path('appointments/<int:appointmentId>', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointments/<int:appointmentId>/cancel', AppointmentCancelView.as_view(), name='appointment-cancel'),

    # Billing routes
    path('billing', BillingListCreateView.as_view(), name='billing-list-create'),
    path('billing/<int:appointmentId>', BillingDetailView.as_view(), name='billing-detail'),
]
