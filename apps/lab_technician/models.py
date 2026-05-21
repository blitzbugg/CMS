from django.db import models

class TblLabTest(models.Model):
    LabTestId = models.AutoField(primary_key=True)
    TestName = models.CharField(max_length=255)
    Category = models.CharField(max_length=100)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    ReferenceRanges = models.TextField()
    SampleType = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.TestName
