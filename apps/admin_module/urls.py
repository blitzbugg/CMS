from django.urls import path
from apps.admin_module.views import (
    StaffListCreateView, StaffDetailView, StaffDeactivateView,
    DoctorListCreateView, DoctorDetailView, DoctorDeactivateView,
    SpecializationListCreateView, SpecializationDetailView,
    RoleListView, RoleDetailView
)

urlpatterns = [
    # Staff routes
    path('staff', StaffListCreateView.as_view(), name='staff-list-create'),
    path('staff/<int:staffId>', StaffDetailView.as_view(), name='staff-detail'),
    path('staff/<int:staffId>/deactivate', StaffDeactivateView.as_view(), name='staff-deactivate'),

    # Doctor routes
    path('doctors', DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors/<int:doctorId>', DoctorDetailView.as_view(), name='doctor-detail'),
    path('doctors/<int:doctorId>/deactivate', DoctorDeactivateView.as_view(), name='doctor-deactivate'),

    # Specialization routes
    path('specializations', SpecializationListCreateView.as_view(), name='specialization-list-create'),
    path('specializations/<int:specializationId>', SpecializationDetailView.as_view(), name='specialization-detail'),

    # Role routes
    path('roles', RoleListView.as_view(), name='role-list'),
    path('roles/<int:roleId>', RoleDetailView.as_view(), name='role-detail'),
]
