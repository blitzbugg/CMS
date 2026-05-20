from django.db import models
from django.core.exceptions import ValidationError
import re

class TblMembership(models.Model):
    MembershipId = models.AutoField(primary_key=True)
    MembershipName = models.CharField(max_length=100)

    def __str__(self):
        return self.MembershipName


class TblPatient(models.Model):
    PatientId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Contact = models.CharField(max_length=20)
    Age = models.IntegerField()
    Gender = models.CharField(max_length=10)
    Address = models.TextField()
    MembershipId = models.ForeignKey(TblMembership, on_delete=models.PROTECT)

    def clean(self):
        super().clean()
        # Contact / Mobile validation: Must be exactly 10 digits
        if not re.match(r'^\d{10}$', self.Contact):
            raise ValidationError({'Contact': 'Must be a valid 10-digit mobile number'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Name


class TblAppointment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    AppointmentId = models.AutoField(primary_key=True)
    PatientId = models.ForeignKey(TblPatient, on_delete=models.CASCADE)
    DoctorId = models.ForeignKey('admin_module.TblDoctor', on_delete=models.CASCADE)
    AppointmentDate = models.DateField()
    AppointmentTime = models.TimeField()
    TokenNumber = models.IntegerField(blank=True, null=True)
    ConsultationStatus = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        if not self.TokenNumber:
            # Generate token number per doctor per date
            count = TblAppointment.objects.filter(
                DoctorId=self.DoctorId,
                AppointmentDate=self.AppointmentDate
            ).count()
            self.TokenNumber = count + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appt {self.AppointmentId} - Patient {self.PatientId.Name} with Doctor {self.DoctorId.StaffId.Name}"


class TblBilling(models.Model):
    BillingId = models.AutoField(primary_key=True)
    AppointmentId = models.OneToOneField(TblAppointment, on_delete=models.CASCADE)
    ConsultationFee = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    RegistrationCharges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    AdditionalCharges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    BillingDate = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-pull consultation fee from doctor
        if not self.ConsultationFee:
            self.ConsultationFee = self.AppointmentId.DoctorId.ConsultationFee
        
        # Calculate total amount
        self.TotalAmount = self.ConsultationFee + (self.RegistrationCharges or 0) + (self.AdditionalCharges or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill {self.BillingId} for Appointment {self.AppointmentId_id}"
