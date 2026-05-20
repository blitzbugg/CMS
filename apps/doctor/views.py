from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.doctor.models import TblConsultation, TblMedicinePrescription, TblLabTestPrescription
from apps.doctor.serializers import TblConsultationSerializer, TblMedicinePrescriptionSerializer, TblLabTestPrescriptionSerializer

# Consultation Views
class ConsultationCreateView(APIView):
    def post(self, request):
        serializer = TblConsultationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ConsultationPatientListView(APIView):
    def get(self, request, patientId):
        queryset = TblConsultation.objects.filter(AppointmentId__PatientId=patientId)
        serializer = TblConsultationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConsultationDoctorListView(APIView):
    def get(self, request, doctorId):
        queryset = TblConsultation.objects.filter(AppointmentId__DoctorId=doctorId)
        serializer = TblConsultationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConsultationAppointmentDetailView(APIView):
    def get(self, request, appointmentId):
        consultation = get_object_or_404(TblConsultation, AppointmentId=appointmentId)
        serializer = TblConsultationSerializer(consultation)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Medicine Prescription Views
class MedicinePrescriptionCreateView(APIView):
    def post(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = TblMedicinePrescriptionSerializer(data=data, many=True)
        else:
            serializer = TblMedicinePrescriptionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MedicinePrescriptionDetailView(APIView):
    def put(self, request, prescriptionId):
        prescription = get_object_or_404(TblMedicinePrescription, PrescriptionId=prescriptionId)
        serializer = TblMedicinePrescriptionSerializer(prescription, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MedicinePrescriptionAppointmentListView(APIView):
    def get(self, request, appointmentId):
        queryset = TblMedicinePrescription.objects.filter(AppointmentId=appointmentId, IsActive=True)
        serializer = TblMedicinePrescriptionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MedicinePrescriptionPatientListView(APIView):
    def get(self, request, patientId):
        queryset = TblMedicinePrescription.objects.filter(AppointmentId__PatientId=patientId, IsActive=True)
        serializer = TblMedicinePrescriptionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MedicinePrescriptionDoctorListView(APIView):
    def get(self, request, doctorId):
        queryset = TblMedicinePrescription.objects.filter(AppointmentId__DoctorId=doctorId, IsActive=True)
        serializer = TblMedicinePrescriptionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Lab Test Prescription Views
class LabTestPrescriptionCreateView(APIView):
    def post(self, request):
        data = request.data
        if isinstance(data, list):
            serializer = TblLabTestPrescriptionSerializer(data=data, many=True)
        else:
            serializer = TblLabTestPrescriptionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LabTestPrescriptionDetailView(APIView):
    def put(self, request, prescriptionId):
        prescription = get_object_or_404(TblLabTestPrescription, LabTestPrescriptionId=prescriptionId)
        serializer = TblLabTestPrescriptionSerializer(prescription, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LabTestPrescriptionAppointmentListView(APIView):
    def get(self, request, appointmentId):
        queryset = TblLabTestPrescription.objects.filter(AppointmentId=appointmentId, IsActive=True)
        serializer = TblLabTestPrescriptionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LabTestPrescriptionPatientListView(APIView):
    def get(self, request, patientId):
        queryset = TblLabTestPrescription.objects.filter(AppointmentId__PatientId=patientId, IsActive=True)
        serializer = TblLabTestPrescriptionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
