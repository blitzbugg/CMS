from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.lab_technician.models import TblLabTest
from apps.doctor.models import TblLabTestPrescription
from apps.lab_technician.serializers import TblLabTestSerializer, TblLabTestResultSerializer

# Lab Test Views
class LabTestListCreateView(APIView):
    def get(self, request):
        queryset = TblLabTest.objects.filter(is_active=True)
        serializer = TblLabTestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TblLabTestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LabTestDetailView(APIView):
    def get(self, request, labTestId):
        lab_test = get_object_or_404(TblLabTest, LabTestId=labTestId)
        serializer = TblLabTestSerializer(lab_test)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, labTestId):
        lab_test = get_object_or_404(TblLabTest, LabTestId=labTestId)
        serializer = TblLabTestSerializer(lab_test, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LabTestDeactivateView(APIView):
    def patch(self, request, labTestId):
        lab_test = get_object_or_404(TblLabTest, LabTestId=labTestId)
        lab_test.is_active = False
        lab_test.save()
        return Response({"message": "Lab test deactivated successfully"}, status=status.HTTP_200_OK)


# Lab Results Views
class LabTestResultAppointmentView(APIView):
    def get(self, request, appointmentId):
        queryset = TblLabTestPrescription.objects.filter(AppointmentId=appointmentId, is_active=True)
        serializer = TblLabTestResultSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LabTestResultListView(APIView):
    def get(self, request):
        start_date = request.query_params.get('startDate')
        end_date = request.query_params.get('endDate')
        queryset = TblLabTestPrescription.objects.filter(is_active=True)
        if start_date and end_date:
            queryset = queryset.filter(AppointmentId__AppointmentDate__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(AppointmentId__AppointmentDate__gte=start_date)
        elif end_date:
            queryset = queryset.filter(AppointmentId__AppointmentDate__lte=end_date)
        serializer = TblLabTestResultSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LabTestResultRecordView(APIView):
    def put(self, request, labTestPrescriptionId):
        prescription = get_object_or_404(TblLabTestPrescription, LabTestPrescriptionId=labTestPrescriptionId)
        serializer = TblLabTestResultSerializer(prescription, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LabTestPrescriptionDeactivateView(APIView):
    def patch(self, request, labTestPrescriptionId):
        prescription = get_object_or_404(TblLabTestPrescription, LabTestPrescriptionId=labTestPrescriptionId)
        prescription.is_active = False
        prescription.save()
        return Response({"message": "Lab test prescription entry deactivated successfully"}, status=status.HTTP_200_OK)
