from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class TblRole(models.Model):
    RoleId = models.AutoField(primary_key=True)
    RoleName = models.CharField(max_length=100)

    def __str__(self):
        return self.RoleName


class TblStaffManager(BaseUserManager):
    def create_user(self, Username, Password=None, **extra_fields):
        if not Username:
            raise ValueError('The Username field must be set')
        user = self.model(Username=Username, **extra_fields)
        if Password:
            user.set_password(Password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Username, Password=None, **extra_fields):
        role, _ = TblRole.objects.get_or_create(RoleName='Administrator')
        extra_fields.setdefault('RoleId', role)
        extra_fields.setdefault('Name', Username)
        extra_fields.setdefault('Contact', '0000000000')
        extra_fields.setdefault('Gender', 'Male')
        extra_fields.setdefault('Address', 'System Generated Superuser')
        extra_fields.setdefault('Salary', 0.00)
        extra_fields.setdefault('EmpID', f"EMP-SU-{Username}")
        return self.create_user(Username, Password, **extra_fields)



class TblStaff(AbstractBaseUser):
    StaffId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Contact = models.CharField(max_length=20)
    Gender = models.CharField(max_length=10)
    Address = models.TextField()
    Salary = models.DecimalField(max_digits=10, decimal_places=2)
    EmpID = models.CharField(max_length=50, unique=True)
    Username = models.CharField(max_length=150, unique=True)
    RoleId = models.ForeignKey(TblRole, on_delete=models.PROTECT)
    IsActive = models.BooleanField(default=True)

    objects = TblStaffManager()

    USERNAME_FIELD = 'Username'
    REQUIRED_FIELDS = ['Name', 'EmpID']

    @property
    def is_active(self):
        return self.IsActive

    @is_active.setter
    def is_active(self, value):
        self.IsActive = value

    @property
    def is_staff(self):
        return True

    @property
    def is_superuser(self):
        return self.RoleId.RoleName == 'Administrator'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def id(self):
        return self.StaffId

    def __str__(self):
        return self.Name


class TblSpecialization(models.Model):
    SpecializationId = models.AutoField(primary_key=True)
    SpecializationName = models.CharField(max_length=255)

    def __str__(self):
        return self.SpecializationName


class TblDoctor(models.Model):
    DoctorId = models.AutoField(primary_key=True)
    StaffId = models.OneToOneField(TblStaff, on_delete=models.CASCADE)
    SpecializationId = models.ForeignKey(TblSpecialization, on_delete=models.PROTECT)
    ConsultationFee = models.DecimalField(max_digits=10, decimal_places=2)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.StaffId.Name}"
