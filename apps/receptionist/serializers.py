import re
from rest_framework import serializers
from apps.receptionist.models import TblMembership, TblPatient, TblAppointment, TblBilling
from apps.admin_module.models import TblDoctor

class TblMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblMembership
        fields = '__all__'


class TblPatientSerializer(serializers.ModelSerializer):
    MembershipName = serializers.CharField(source='MembershipId.MembershipName', read_only=True)

    class Meta:
        model = TblPatient
        fields = ['PatientId', 'Name', 'Contact', 'Age', 'Gender', 'Address', 'MembershipId', 'MembershipName']

    def validate_Contact(self, value):
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("Must be a valid 10-digit mobile number")
        return value


class TblAppointmentSerializer(serializers.ModelSerializer):
    PatientName = serializers.CharField(source='PatientId.Name', read_only=True)
    DoctorName = serializers.CharField(source='DoctorId.StaffId.Name', read_only=True)

    class Meta:
        model = TblAppointment
        fields = ['AppointmentId', 'PatientId', 'PatientName', 'DoctorId', 'DoctorName', 'AppointmentDate', 'AppointmentTime', 'TokenNumber', 'ConsultationStatus']
        read_only_fields = ['TokenNumber']

    def validate_DoctorId(self, value):
        # Business Rule 2: Doctor availability check
        if not value.is_active:
            raise serializers.ValidationError("Selected doctor is not active.")
        return value


class TblBillingSerializer(serializers.ModelSerializer):
    TotalAmount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    ConsultationFee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = TblBilling
        fields = ['BillingId', 'AppointmentId', 'ConsultationFee', 'RegistrationCharges', 'AdditionalCharges', 'TotalAmount', 'BillingDate']
