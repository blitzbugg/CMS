import re
from rest_framework import serializers
from apps.admin_module.models import TblRole, TblStaff, TblSpecialization, TblDoctor

class TblRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblRole
        fields = '__all__'


class TblSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblSpecialization
        fields = '__all__'


class TblStaffSerializer(serializers.ModelSerializer):
    RoleName = serializers.CharField(source='RoleId.RoleName', read_only=True)
    Password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = TblStaff
        fields = ['StaffId', 'Name', 'Contact', 'Gender', 'Address', 'Salary', 'EmpID', 'Username', 'Password', 'RoleId', 'RoleName', 'is_active']

    def validate_Contact(self, value):
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("Must be a valid 10-digit mobile number")
        return value

    def create(self, validated_data):
        password = validated_data.get('Password')
        # DRF automatically performs unique validation on Username and EmpID because they are marked unique in models
        staff = TblStaff.objects.create_user(
            Username=validated_data['Username'],
            Password=password,
            Name=validated_data.get('Name', ''),
            Contact=validated_data.get('Contact', ''),
            Gender=validated_data.get('Gender', ''),
            Address=validated_data.get('Address', ''),
            Salary=validated_data.get('Salary', 0.00),
            EmpID=validated_data.get('EmpID', ''),
            RoleId=validated_data.get('RoleId'),
            is_active=validated_data.get('is_active', True)
        )
        return staff

    def update(self, instance, validated_data):
        password = validated_data.pop('Password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class TblDoctorSerializer(serializers.ModelSerializer):
    StaffDetails = TblStaffSerializer(source='StaffId', read_only=True)
    SpecializationName = serializers.CharField(source='SpecializationId.SpecializationName', read_only=True)

    class Meta:
        model = TblDoctor
        fields = ['DoctorId', 'StaffId', 'StaffDetails', 'SpecializationId', 'SpecializationName', 'ConsultationFee', 'IsActive']
