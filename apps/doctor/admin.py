from django.contrib import admin
from apps.doctor.models import TblConsultation, TblMedicinePrescription, TblLabTestPrescription

admin.site.register(TblConsultation)
admin.site.register(TblMedicinePrescription)
admin.site.register(TblLabTestPrescription)
