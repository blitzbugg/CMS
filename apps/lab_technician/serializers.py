from rest_framework import serializers
from apps.lab_technician.models import TblLabTest
from apps.doctor.models import TblLabTestPrescription

class TblLabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblLabTest
        fields = '__all__'


class TblLabTestResultSerializer(serializers.ModelSerializer):
    TestName = serializers.CharField(source='LabTestId.TestName', read_only=True)

    class Meta:
        model = TblLabTestPrescription
        fields = ['LabTestPrescriptionId', 'AppointmentId', 'LabTestId', 'TestName', 'Instructions', 'LabTestValue', 'Remarks', 'IsActive']
        read_only_fields = ['AppointmentId', 'LabTestId', 'Instructions']
