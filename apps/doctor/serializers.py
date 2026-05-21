from rest_framework import serializers
from apps.doctor.models import TblConsultation, TblMedicinePrescription, TblLabTestPrescription

class TblConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblConsultation
        fields = '__all__'


class TblMedicinePrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblMedicinePrescription
        fields = '__all__'


class TblLabTestPrescriptionSerializer(serializers.ModelSerializer):
    TestName = serializers.CharField(source='LabTestId.TestName', read_only=True)

    class Meta:
        model = TblLabTestPrescription
        fields = ['LabTestPrescriptionId', 'AppointmentId', 'LabTestId', 'TestName', 'Instructions', 'LabTestValue', 'Remarks', 'is_active']
