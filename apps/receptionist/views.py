from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.receptionist.models import TblPatient, TblAppointment, TblBilling
from apps.receptionist.serializers import TblPatientSerializer, TblAppointmentSerializer, TblBillingSerializer

# Patient Views
class PatientListCreateView(APIView):
    def get(self, request):
        name = request.query_params.get('name')
        patient_id = request.query_params.get('id')
        mobile = request.query_params.get('mobile')
        queryset = TblPatient.objects.all()
        if name:
            queryset = queryset.filter(Name__icontains=name)
        if patient_id:
            queryset = queryset.filter(PatientId=patient_id)
        if mobile:
            queryset = queryset.filter(Contact__icontains=mobile)
        serializer = TblPatientSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TblPatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PatientDetailView(APIView):
    def get(self, request, patientId):
        patient = get_object_or_404(TblPatient, PatientId=patientId)
        serializer = TblPatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, patientId):
        patient = get_object_or_404(TblPatient, PatientId=patientId)
        serializer = TblPatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Appointment Views
class AppointmentListCreateView(APIView):
    def get(self, request):
        date = request.query_params.get('date')
        status_param = request.query_params.get('status')
        queryset = TblAppointment.objects.all()
        if date:
            queryset = queryset.filter(AppointmentDate=date)
        if status_param:
            queryset = queryset.filter(ConsultationStatus=status_param)
        serializer = TblAppointmentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TblAppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AppointmentPatientListView(APIView):
    def get(self, request, patientId):
        queryset = TblAppointment.objects.filter(PatientId=patientId)
        serializer = TblAppointmentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentDoctorListView(APIView):
    def get(self, request, doctorId):
        queryset = TblAppointment.objects.filter(DoctorId=doctorId)
        serializer = TblAppointmentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentDetailView(APIView):
    def put(self, request, appointmentId):
        appointment = get_object_or_404(TblAppointment, AppointmentId=appointmentId)
        serializer = TblAppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AppointmentCancelView(APIView):
    def patch(self, request, appointmentId):
        appointment = get_object_or_404(TblAppointment, AppointmentId=appointmentId)
        appointment.ConsultationStatus = 'Cancelled'
        appointment.save()
        return Response({"message": "Appointment cancelled successfully"}, status=status.HTTP_200_OK)


# Billing Views
class BillingListCreateView(APIView):
    def get(self, request):
        start_date = request.query_params.get('startDate')
        end_date = request.query_params.get('endDate')
        queryset = TblBilling.objects.all()
        if start_date and end_date:
            queryset = queryset.filter(BillingDate__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(BillingDate__gte=start_date)
        elif end_date:
            queryset = queryset.filter(BillingDate__lte=end_date)
        serializer = TblBillingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Prevent generating duplicate bill for the same appointment since Billing is OneToOne
        appt_id = request.data.get('AppointmentId')
        if TblBilling.objects.filter(AppointmentId=appt_id).exists():
            return Response({"error": "Bill already generated for this appointment"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TblBillingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BillingDetailView(APIView):
    def get(self, request, appointmentId):
        billing = get_object_or_404(TblBilling, AppointmentId=appointmentId)
        serializer = TblBillingSerializer(billing)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, appointmentId):
        billing = get_object_or_404(TblBilling, AppointmentId=appointmentId)
        serializer = TblBillingSerializer(billing, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
