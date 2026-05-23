# AGENT.md — MacFast CMS Backend

## Project Overview

Build the **MacFast Clinic Management System (CMS)** backend — a Django REST Framework application backed by SQLite. This is a **local academic project**, not a production system. Keep it simple, clean, and fully functional.

---

## Tech Stack

| Layer        | Technology                        |
|--------------|-----------------------------------|
| Framework    | Django + Django REST Framework    |
| Database     | SQLite (default Django db.sqlite3)|
| Auth         | JWT via `djangorestframework-simplejwt` |
| Language     | Python 3.x                        |

No Docker. No Celery. No Redis. No external services. Just `python manage.py runserver`.

---

## Project Structure

```
macfast_cms/
├── manage.py
├── db.sqlite3
├── macfast_cms/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── auth_module/       # Login, logout, JWT
│   ├── admin_module/      # Staff, Doctors, Roles, Specializations
│   ├── receptionist/      # Patients, Appointments, Billing
│   ├── doctor/            # Consultations, Medicine Prescriptions, Lab Test Prescriptions
│   ├── pharmacist/        # Medicines, Inventory
│   └── lab_technician/    # Lab Tests, Results
```

---

## Database Models

Define these models. Use SQLite-compatible field types. All IDs are auto-generated primary keys unless noted.

### TblRole
| Field    | Type        | Notes                    |
|----------|-------------|--------------------------|
| RoleId   | AutoField PK|                          |
| RoleName | CharField   | e.g. Administrator, Receptionist, Doctor, Pharmacist, Lab Technician |

### TblStaff
| Field       | Type        | Notes                         |
|-------------|-------------|-------------------------------|
| StaffId     | AutoField PK|                               |
| Name        | CharField   |                               |
| Contact     | CharField   |                               |
| Gender      | CharField   |                               |
| Address     | TextField   |                               |
| Salary      | DecimalField|                               |
| EmpID       | CharField   | Unique                        |
| Username    | CharField   | Unique                        |
| Password    | CharField   | Store hashed (use Django's make_password) |
| RoleId      | ForeignKey  | → TblRole                     |
| IsActive    | BooleanField| Default True                  |

### TblSpecialization
| Field              | Type        |
|--------------------|-------------|
| SpecializationId   | AutoField PK|
| SpecializationName | CharField   |

### TblDoctor
| Field            | Type        | Notes                   |
|------------------|-------------|-------------------------|
| DoctorId         | AutoField PK|                         |
| StaffId          | OneToOneField | → TblStaff            |
| SpecializationId | ForeignKey  | → TblSpecialization     |
| ConsultationFee  | DecimalField|                         |
| IsActive         | BooleanField| Default True            |

### TblMembership
| Field          | Type        |
|----------------|-------------|
| MembershipId   | AutoField PK|
| MembershipName | CharField   |

### TblPatient
| Field        | Type        | Notes                          |
|--------------|-------------|--------------------------------|
| PatientId    | AutoField PK|                                |
| Name         | CharField   |                                |
| Contact      | CharField   | Validate mobile number format  |
| Age          | IntegerField|                                |
| Gender       | CharField   |                                |
| Address      | TextField   |                                |
| MembershipId | ForeignKey  | → TblMembership                |

### TblAppointment
| Field              | Type        | Notes                                        |
|--------------------|-------------|----------------------------------------------|
| AppointmentId      | AutoField PK|                                              |
| PatientId          | ForeignKey  | → TblPatient                                 |
| DoctorId           | ForeignKey  | → TblDoctor                                  |
| AppointmentDate    | DateField   |                                              |
| AppointmentTime    | TimeField   |                                              |
| TokenNumber        | IntegerField| Auto-generated per doctor per date           |
| ConsultationStatus | CharField   | Choices: Pending, Completed, Cancelled       |

### TblBilling
| Field               | Type         | Notes                             |
|---------------------|--------------|-----------------------------------|
| BillingId           | AutoField PK |                                   |
| AppointmentId       | OneToOneField| → TblAppointment                  |
| ConsultationFee     | DecimalField | Pulled from TblDoctor             |
| RegistrationCharges | DecimalField |                                   |
| AdditionalCharges   | DecimalField |                                   |
| TotalAmount         | DecimalField | Calculated                        |
| BillingDate         | DateField    | Auto today                        |

### TblConsultation
| Field           | Type        | Notes                     |
|-----------------|-------------|---------------------------|
| ConsultationId  | AutoField PK|                           |
| AppointmentId   | ForeignKey  | → TblAppointment          |
| Symptoms        | TextField   |                           |
| Diagnosis       | TextField   |                           |
| Notes           | TextField   | Optional                  |

### TblMedicinePrescription
| Field          | Type        | Notes                       |
|----------------|-------------|-----------------------------|
| PrescriptionId | AutoField PK|                             |
| AppointmentId  | ForeignKey  | → TblAppointment            |
| MedicineName   | CharField   |                             |
| Dosage         | CharField   |                             |
| Frequency      | CharField   |                             |
| Duration       | CharField   |                             |
| IsActive       | BooleanField| Default True                |

### TblLabTestPrescription
| Field                    | Type        | Notes                      |
|--------------------------|-------------|----------------------------|
| LabTestPrescriptionId    | AutoField PK|                            |
| AppointmentId            | ForeignKey  | → TblAppointment           |
| LabTestId                | ForeignKey  | → TblLabTest               |
| Instructions             | TextField   | Optional                   |
| LabTestValue             | CharField   | Filled by lab technician   |
| Remarks                  | TextField   | Optional, filled by lab tech|
| IsActive                 | BooleanField| Default True               |

### TblMedicine
| Field               | Type        | Notes                   |
|---------------------|-------------|-------------------------|
| MedicineId          | AutoField PK|                         |
| MedicineName        | CharField   |                         |
| Category            | CharField   |                         |
| ManufacturingDate   | DateField   |                         |
| ExpiryDate          | DateField   |                         |
| Unit                | CharField   |                         |
| IsActive            | BooleanField| Default True            |

### TblMedicineStock
| Field           | Type        | Notes                   |
|-----------------|-------------|-------------------------|
| MedicineStockId | AutoField PK|                         |
| MedicineId      | ForeignKey  | → TblMedicine           |
| Quantity        | IntegerField|                         |
| IsLowStock      | BooleanField| Default False           |

### TblLabTest
| Field           | Type        | Notes                   |
|-----------------|-------------|-------------------------|
| LabTestId       | AutoField PK|                         |
| TestName        | CharField   |                         |
| Category        | CharField   |                         |
| Amount          | DecimalField|                         |
| ReferenceRanges | TextField   |                         |
| SampleType      | CharField   |                         |
| IsActive        | BooleanField| Default True            |

---

## Authentication

- Use JWT (`djangorestframework-simplejwt`)
- Login returns `access` and `refresh` tokens
- All endpoints except `/api/auth/login` require a valid Bearer token
- Deactivated staff (`IsActive = False`) must be blocked from logging in
- Seed the following default roles on first run (use a data migration or management command):
  - Administrator
  - Receptionist
  - Doctor
  - Pharmacist
  - Lab Technician

---

## API Endpoints

Implement all endpoints listed below. Use DRF `APIView` or `ViewSet`. Return JSON. Use proper HTTP status codes.

---

### AUTH MODULE

| Method | URL                  | Description                          |
|--------|----------------------|--------------------------------------|
| POST   | `/api/auth/login`    | Login with email/username + password, return JWT tokens |
| POST   | `/api/auth/logout`   | Invalidate token (blacklist refresh token) |

---

### ADMIN MODULE

#### Staff
| Method | URL                                    | Description            |
|--------|----------------------------------------|------------------------|
| POST   | `/api/staff`                           | Create new staff        |
| GET    | `/api/staff`                           | List all staff (supports filter by name or role) |
| GET    | `/api/staff/{staffId}`                 | Get staff by ID         |
| PUT    | `/api/staff/{staffId}`                 | Update staff            |
| PATCH  | `/api/staff/{staffId}/deactivate`      | Deactivate staff (soft delete, IsActive=0) |

#### Doctors
| Method | URL                                     | Description                  |
|--------|-----------------------------------------|------------------------------|
| POST   | `/api/doctors`                          | Create doctor profile (link to staff) |
| GET    | `/api/doctors`                          | List all active doctors       |
| GET    | `/api/doctors/{doctorId}`               | Get doctor by ID              |
| PUT    | `/api/doctors/{doctorId}`               | Update doctor                 |
| PATCH  | `/api/doctors/{doctorId}/deactivate`    | Deactivate doctor             |

#### Specializations
| Method | URL                                             | Description              |
|--------|-------------------------------------------------|--------------------------|
| POST   | `/api/specializations`                          | Add specialization        |
| PUT    | `/api/specializations/{specializationId}`       | Update specialization     |
| GET    | `/api/specializations`                          | List all specializations  |

#### Roles
| Method | URL                        | Description         |
|--------|----------------------------|---------------------|
| GET    | `/api/roles`               | List all roles       |
| GET    | `/api/roles/{roleId}`      | Get role by ID       |

---

### RECEPTIONIST MODULE

#### Patients
| Method | URL                             | Description                              |
|--------|---------------------------------|------------------------------------------|
| POST   | `/api/patients`                 | Register new patient                      |
| GET    | `/api/patients`                 | List all patients (filter by name/ID/mobile) |
| GET    | `/api/patients/{patientId}`     | Get patient by ID                         |
| PUT    | `/api/patients/{patientId}`     | Update patient                            |

#### Appointments
| Method | URL                                            | Description                         |
|--------|------------------------------------------------|-------------------------------------|
| POST   | `/api/appointments`                            | Schedule appointment, auto-generate TokenNumber |
| GET    | `/api/appointments?date={date}`                | List appointments by date            |
| GET    | `/api/appointments?status={status}`            | List appointments by status          |
| GET    | `/api/appointments/patient/{patientId}`        | List appointments for a patient      |
| GET    | `/api/appointments/doctor/{doctorId}`          | List appointments for a doctor       |
| PUT    | `/api/appointments/{appointmentId}`            | Update appointment                   |
| PATCH  | `/api/appointments/{appointmentId}/cancel`     | Cancel appointment (ConsultationStatus = 'Cancelled') |

#### Billing
| Method | URL                                      | Description                         |
|--------|------------------------------------------|-------------------------------------|
| POST   | `/api/billing`                           | Generate consultation bill           |
| GET    | `/api/billing/{appointmentId}`           | Get bill by appointment              |
| PUT    | `/api/billing/{appointmentId}`           | Update bill                          |
| GET    | `/api/billing?startDate=&endDate=`       | List bills within a date range       |

---

### DOCTOR MODULE

#### Consultations
| Method | URL                                                      | Description                        |
|--------|----------------------------------------------------------|------------------------------------|
| POST   | `/api/consultations`                                     | Add consultation note (linked to appointment) |
| GET    | `/api/consultations/patient/{patientId}`                 | List consultation history by patient |
| GET    | `/api/consultations/doctor/{doctorId}`                   | List consultation history by doctor |
| GET    | `/api/consultations/history/appointment/{appointmentId}` | Get consultation by appointment     |

#### Medicine Prescriptions
| Method | URL                                                          | Description                              |
|--------|--------------------------------------------------------------|------------------------------------------|
| POST   | `/api/prescriptions/medicine`                                | Create medicine prescription (multiple medicines per appointment) |
| PUT    | `/api/prescriptions/medicine/{prescriptionId}`               | Update a prescription entry              |
| GET    | `/api/prescriptions/medicine/appointment/{appointmentId}`    | Get prescriptions for an appointment     |
| GET    | `/api/prescriptions/medicine/patient/{patientId}`            | List prescriptions for a patient         |
| GET    | `/api/prescriptions/medicine/history/patient/{patientId}`    | Full prescription history by patient     |
| GET    | `/api/prescriptions/medicine/history/doctor/{doctorId}`      | Full prescription history by doctor      |

#### Lab Test Prescriptions
| Method | URL                                                        | Description                              |
|--------|------------------------------------------------------------|------------------------------------------|
| POST   | `/api/prescriptions/labtest`                               | Prescribe lab tests (multiple per appointment) |
| PUT    | `/api/prescriptions/labtest/{prescriptionId}`              | Update lab test prescription             |
| GET    | `/api/prescriptions/labtest/appointment/{appointmentId}`   | Get lab prescriptions for an appointment |
| GET    | `/api/prescriptions/labtest/patient/{patientId}`           | List lab prescriptions by patient        |

---

### PHARMACIST MODULE

#### Medicines
| Method | URL                                        | Description              |
|--------|--------------------------------------------|--------------------------|
| POST   | `/api/medicines`                           | Add new medicine          |
| GET    | `/api/medicines`                           | List all medicines        |
| GET    | `/api/medicines/{medicineId}`              | Get medicine by ID        |
| PUT    | `/api/medicines/{medicineId}`              | Update medicine           |
| PATCH  | `/api/medicines/{medicineId}/deactivate`   | Deactivate medicine       |

#### Inventory
| Method | URL                                                      | Description                            |
|--------|----------------------------------------------------------|----------------------------------------|
| POST   | `/api/inventory/medicine`                                | Add inventory item                      |
| GET    | `/api/inventory/medicine`                                | List all inventory                      |
| GET    | `/api/inventory/medicine/{medicineId}`                   | Get stock for a specific medicine       |
| PUT    | `/api/inventory/medicine/{medicineStockId}`              | Update stock quantity                   |
| PATCH  | `/api/inventory/medicine/{medicineStockId}/flag-low`     | Flag item as low stock                  |

---

### LAB TECHNICIAN MODULE

#### Lab Tests
| Method | URL                                        | Description               |
|--------|--------------------------------------------|---------------------------|
| POST   | `/api/labtests`                            | Add new lab test            |
| GET    | `/api/labtests`                            | List all lab tests          |
| GET    | `/api/labtests/{labTestId}`                | Get lab test by ID          |
| PUT    | `/api/labtests/{labTestId}`                | Update lab test             |
| PATCH  | `/api/labtests/{labTestId}/deactivate`     | Deactivate lab test         |

#### Lab Test Results
| Method | URL                                                          | Description                              |
|--------|--------------------------------------------------------------|------------------------------------------|
| GET    | `/api/labtests/results/appointment/{appointmentId}`          | Get lab results for an appointment        |
| GET    | `/api/labtests/results?startDate=&endDate=`                  | List results within a date range          |
| PUT    | `/api/labtests/results/{labTestPrescriptionId}`              | Record/update lab result (LabTestValue + Remarks) |
| PATCH  | `/api/labtests/{labTestPrescriptionId}/deactivate`           | Deactivate a lab test prescription entry |

---

## Business Logic — Key Rules

1. **Token Number**: When scheduling an appointment, auto-generate a `TokenNumber` by counting existing appointments for the same doctor on the same date and incrementing by 1.

2. **Doctor availability**: Before booking an appointment, check that the doctor is active (`IsActive = True` in TblDoctor).

3. **Deactivated staff cannot log in**: During login, check `IsActive` on TblStaff. Return 401 if inactive.

4. **Consultation Fee in Billing**: When generating a bill (`POST /api/billing`), auto-pull the `ConsultationFee` from TblDoctor based on the appointment's DoctorId.

5. **Soft Deletes**: Never hard-delete anything. Use `IsActive = False` for staff, doctors, medicines, and lab tests.

6. **Multiple prescriptions per appointment**: Both `TblMedicinePrescription` and `TblLabTestPrescription` support multiple rows per `AppointmentId`.

7. **Stock update on dispensing**: When a pharmacist dispenses medicine, subtract the quantity from `TblMedicineStock`.

8. **Bill total calculation**: `TotalAmount = ConsultationFee + RegistrationCharges + AdditionalCharges`.

---

## Validation Requirements

| Field               | Rule                                                      |
|---------------------|-----------------------------------------------------------|
| Contact / Mobile    | Must be a valid 10-digit mobile number                    |
| Required fields     | Return 400 Bad Request with field-level error messages    |
| Duplicate EmpID     | Return 400 if EmpID already exists                        |
| Duplicate username  | Return 400 on staff create/update if username is taken    |
| AppointmentDate     | Must be a valid date                                      |
| ExpiryDate          | Should be after ManufacturingDate for medicines           |

---

## Error Responses

Use consistent JSON error format:

```json
{
  "error": "Description of what went wrong"
}
```

Or for field-level validation:

```json
{
  "errors": {
    "field_name": ["error message"]
  }
}
```

---

## Expected HTTP Status Codes

| Scenario                  | Status Code |
|---------------------------|-------------|
| Successful creation        | 201 Created |
| Successful retrieval/update| 200 OK      |
| Validation failure         | 400 Bad Request |
| Unauthenticated request    | 401 Unauthorized |
| Resource not found         | 404 Not Found |
| Deactivated account login  | 401 Unauthorized |

---

## Setup Instructions to Generate

At the end of building the project, provide a `README.md` with:

```bash
# Install dependencies
pip install django djangorestframework djangorestframework-simplejwt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Seed default roles
python manage.py seed_roles

# Create superuser (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## Seed Data

Create a management command `seed_roles` that inserts the five default roles if they don't already exist:
- Administrator
- Receptionist
- Doctor
- Pharmacist
- Lab Technician

Also seed at least one default membership type (e.g., "General") for patient registration.

---

## What NOT to Do

- Do NOT set up Docker or any containerization
- Do NOT use PostgreSQL or any external database — SQLite only
- Do NOT build a frontend — backend API only
- Do NOT add Celery, Redis, or any async task queue
- Do NOT use `django-allauth` or any third-party auth beyond `simplejwt`
- Do NOT add pagination unless explicitly needed — keep it simple
- Do NOT over-engineer — this is an academic project running locally

---

## Deliverables Checklist

- [x] Django project initialized with the app structure above
- [x] All models defined and migrations created
- [x] JWT authentication working (login/logout)
- [x] All 5 modules' endpoints implemented and returning correct responses
- [x] Seed management command for roles and membership
- [x] Business logic rules implemented (token number, fee auto-pull, soft deletes, stock updates)
- [x] `README.md` with setup steps