from django.contrib import admin
from apps.receptionist.models import TblMembership, TblPatient, TblAppointment, TblBilling

admin.site.register(TblMembership)
admin.site.register(TblPatient)
admin.site.register(TblAppointment)
admin.site.register(TblBilling)
