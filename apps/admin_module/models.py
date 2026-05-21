from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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
        extra_fields.setdefault('is_staff', True)       # <-- add this
        extra_fields.setdefault('is_superuser', True)   # <-- add this
        role, _ = TblRole.objects.get_or_create(RoleName='Administrator')
        extra_fields.setdefault('RoleId', role)
        extra_fields.setdefault('Name', Username)
        extra_fields.setdefault('Contact', '0000000000')
        extra_fields.setdefault('Gender', 'Male')
        extra_fields.setdefault('Address', 'System Generated Superuser')
        extra_fields.setdefault('Salary', 0.00)
        extra_fields.setdefault('EmpID', f"EMP-SU-{Username}")
        return self.create_user(Username, Password, **extra_fields)


class TblStaff(AbstractBaseUser, PermissionsMixin):
    StaffId  = models.AutoField(primary_key=True)
    Name     = models.CharField(max_length=255)
    Contact  = models.CharField(max_length=20)
    Gender   = models.CharField(max_length=10)
    Address  = models.TextField()
    Salary   = models.DecimalField(max_digits=10, decimal_places=2)
    EmpID    = models.CharField(max_length=50, unique=True)
    Username = models.CharField(max_length=150, unique=True)
    RoleId   = models.ForeignKey(TblRole, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    # PermissionsMixin needs these as real DB columns
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = TblStaffManager()

    USERNAME_FIELD  = 'Username'
    REQUIRED_FIELDS = ['Name', 'EmpID']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def id(self):
        return self.StaffId

    def __str__(self):
        return self.Name


class TblSpecialization(models.Model):
    SpecializationId   = models.AutoField(primary_key=True)
    SpecializationName = models.CharField(max_length=255)

    def __str__(self):
        return self.SpecializationName


class TblDoctor(models.Model):
    DoctorId         = models.AutoField(primary_key=True)
    StaffId          = models.OneToOneField(TblStaff, on_delete=models.CASCADE)
    SpecializationId = models.ForeignKey(TblSpecialization, on_delete=models.PROTECT)
    ConsultationFee  = models.DecimalField(max_digits=10, decimal_places=2)
    IsActive         = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.StaffId.Name}"