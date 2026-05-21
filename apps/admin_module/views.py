from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.admin_module.models import TblRole, TblStaff, TblSpecialization, TblDoctor
from apps.admin_module.serializers import TblRoleSerializer, TblStaffSerializer, TblSpecializationSerializer, TblDoctorSerializer

# Staff Views
class StaffListCreateView(APIView):
    def get(self, request):
        name = request.query_params.get('name')
        role = request.query_params.get('role')
        queryset = TblStaff.objects.all()
        if name:
            queryset = queryset.filter(Name__icontains=name)
        if role:
            queryset = queryset.filter(RoleId__RoleName__icontains=role)
        serializer = TblStaffSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TblStaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class StaffDetailView(APIView):
    def get(self, request, staffId):
        staff = get_object_or_404(TblStaff, StaffId=staffId)
        serializer = TblStaffSerializer(staff)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, staffId):
        staff = get_object_or_404(TblStaff, StaffId=staffId)
        serializer = TblStaffSerializer(staff, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class StaffDeactivateView(APIView):
    def patch(self, request, staffId):
        staff = get_object_or_404(TblStaff, StaffId=staffId)
        staff.is_active = False
        staff.save()
        return Response({"message": "Staff member deactivated successfully"}, status=status.HTTP_200_OK)


# Doctor Views
class DoctorListCreateView(APIView):
    def get(self, request):
        queryset = TblDoctor.objects.filter(IsActive=True)
        serializer = TblDoctorSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TblDoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DoctorDetailView(APIView):
    def get(self, request, doctorId):
        doctor = get_object_or_404(TblDoctor, DoctorId=doctorId)
        serializer = TblDoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, doctorId):
        doctor = get_object_or_404(TblDoctor, DoctorId=doctorId)
        serializer = TblDoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DoctorDeactivateView(APIView):
    def patch(self, request, doctorId):
        doctor = get_object_or_404(TblDoctor, DoctorId=doctorId)
        doctor.IsActive = False
        doctor.save()
        return Response({"message": "Doctor deactivated successfully"}, status=status.HTTP_200_OK)


# Specialization Views
class SpecializationListCreateView(APIView):
    def get(self, request):
        queryset = TblSpecialization.objects.all()
        serializer = TblSpecializationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TblSpecializationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SpecializationDetailView(APIView):
    def put(self, request, specializationId):
        specialization = get_object_or_404(TblSpecialization, SpecializationId=specializationId)
        serializer = TblSpecializationSerializer(specialization, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Role Views
class RoleListView(APIView):
    def get(self, request):
        queryset = TblRole.objects.all()
        serializer = TblRoleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleDetailView(APIView):
    def get(self, request, roleId):
        role = get_object_or_404(TblRole, RoleId=roleId)
        serializer = TblRoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)
