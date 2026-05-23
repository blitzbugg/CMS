from django.db import models

class TblConsultation(models.Model):
    ConsultationId = models.AutoField(primary_key=True)
    AppointmentId = models.ForeignKey('receptionist.TblAppointment', on_delete=models.CASCADE)
    Symptoms = models.TextField()
    Diagnosis = models.TextField()
    Notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Consultation {self.ConsultationId} for Appointment {self.AppointmentId_id}"


class TblMedicinePrescription(models.Model):
    PrescriptionId = models.AutoField(primary_key=True)
    AppointmentId = models.ForeignKey('receptionist.TblAppointment', on_delete=models.CASCADE)
    MedicineName = models.CharField(max_length=255)
    Dosage = models.CharField(max_length=100)
    Frequency = models.CharField(max_length=100)
    Duration = models.CharField(max_length=100)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return f"Prescription {self.PrescriptionId} for Appt {self.AppointmentId_id} - {self.MedicineName}"


class TblLabTestPrescription(models.Model):
    LabTestPrescriptionId = models.AutoField(primary_key=True)
    AppointmentId = models.ForeignKey('receptionist.TblAppointment', on_delete=models.CASCADE)
    LabTestId = models.ForeignKey('lab_technician.TblLabTest', on_delete=models.CASCADE)
    Instructions = models.TextField(blank=True, null=True)
    LabTestValue = models.CharField(max_length=255, blank=True, null=True)
    Remarks = models.TextField(blank=True, null=True)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return f"LabPrescription {self.LabTestPrescriptionId} for Appt {self.AppointmentId_id} - Test {self.LabTestId_id}"
