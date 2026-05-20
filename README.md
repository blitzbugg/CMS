# MacFast Clinic Management System (CMS) Backend

A professional, high-performance local academic Django REST Framework (DRF) backend for the **MacFast Clinic Management System (CMS)**. 

This backend system uses an SQLite database, runs locally, implements full JWT authentication, and follows a clean modular app architecture.

---

## 🚀 Setup Instructions

Follow these simple steps to set up and run the backend locally:

### 1. Install Dependencies
Make sure you have Python 3.x installed, then install the required libraries:
```bash
pip install django djangorestframework djangorestframework-simplejwt
```

### 2. Run Migrations
Run the database migration commands to set up the SQLite database and create all required tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Seed Default Roles & Memberships
We have built a custom management command to seed the system with mandatory roles and default memberships:
```bash
python manage.py seed_roles
```
*Seeds:*
*   **Roles:** `Administrator`, `Receptionist`, `Doctor`, `Pharmacist`, `Lab Technician`
*   **Memberships:** `General`, `Premium`, `VIP`

### 4. Create Superuser (Optional)
Create an administrative account to access the Django Admin interface. Our custom User Manager will automatically handle and supply default values for the database constraints:
```bash
python manage.py createsuperuser
```

### 5. Run Server
Start the local development server:
```bash
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.

---

## 📂 Project Architecture & Modules

The backend is structured into modular, domain-specific apps inside the `apps/` directory:

```
macfast_cms/
├── manage.py
├── db.sqlite3
├── macfast_cms/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── apps/
    ├── auth_module/       # Login, logout, and token blacklisting
    ├── admin_module/      # Staff, Doctors, Roles, and Specializations
    ├── receptionist/      # Patients, Appointments, and Billing
    ├── doctor/            # Consultations, Medicines, and Lab prescriptions
    ├── pharmacist/        # Medicines inventory and stock tracking
    └── lab_technician/    # Lab tests and result entry
```

---

## 🔒 Authentication

All endpoints in the backend (except `/api/auth/login`) are secured by default with **JWT Bearer Token** authentication:
*   Add `Authorization: Bearer <your_access_token>` in the HTTP headers of your requests.
*   **Deactivated accounts:** Inactive staff (`IsActive = False`) are blocked automatically during login and will receive a `401 Unauthorized` response.
*   **Logout:** Validating security, the `/api/auth/logout` endpoint will blacklist the provided refresh token.

---

## ⚡ Core Business Logic & Rules Implemented

1.  **Token Number Auto-generation:** When scheduling a new appointment, the backend automatically counts existing appointments for that doctor on that date, incrementing the value by 1, and saves it in `TokenNumber`.
2.  **Doctor Availability Check:** Before registering an appointment, the system checks whether the doctor's status is active (`IsActive = True`).
3.  **Soft Deletes:** Deactivating staff, doctors, patients, medicines, and lab tests does not erase them from the database. It sets `IsActive = False` (soft delete) to preserve historical data.
4.  **Automatic Fee Pulling & Total Calculation:**
    *   Creating a bill automatically pulls the `ConsultationFee` from the respective doctor's profile.
    *   Calculates the total amount as: `TotalAmount = ConsultationFee + RegistrationCharges + AdditionalCharges`.
5.  **Stock Dispensing Logic:** In the Pharmacist module, we added a custom `/api/inventory/medicine/dispense` endpoint that automatically subtracts dispensed quantities from `TblMedicineStock` and flags low stock if the quantity drops below `10`.

---

## 📋 Complete API Endpoints List

### 🔑 Authentication Module
*   `POST /api/auth/login` — Login with username + password, returns JWT access and refresh tokens.
*   `POST /api/auth/logout` — Logs out by blacklisting the refresh token.

### 👤 Admin Module
*   `GET /api/staff` — List all staff members (supports optional filtering by `name` or `role`).
*   `POST /api/staff` — Create a new staff member (hashes passwords automatically).
*   `GET /api/staff/{staffId}` — Retrieve staff details by ID.
*   `PUT /api/staff/{staffId}` — Update staff details.
*   `PATCH /api/staff/{staffId}/deactivate` — Soft-deactivates staff (`IsActive = False`).
*   `GET /api/doctors` — List all active doctor profiles.
*   `POST /api/doctors` — Create doctor profile linked to staff.
*   `GET /api/doctors/{doctorId}` — Retrieve doctor details.
*   `PUT /api/doctors/{doctorId}` — Update doctor details.
*   `PATCH /api/doctors/{doctorId}/deactivate` — Soft-deactivates doctor.
*   `GET /api/specializations` — List all specializations.
*   `POST /api/specializations` — Create a new specialization.
*   `PUT /api/specializations/{specializationId}` — Update a specialization.
*   `GET /api/roles` — List all roles.
*   `GET /api/roles/{roleId}` — Get role by ID.

### 📋 Receptionist Module
*   `GET /api/patients` — List all patients (supports filtering by `name`, `id`, or `mobile`).
*   `POST /api/patients` — Register a new patient (validates 10-digit mobile number format).
*   `GET /api/patients/{patientId}` — Retrieve patient details.
*   `PUT /api/patients/{patientId}` — Update patient details.
*   `GET /api/appointments` — List appointments (supports filtering by `date` or `status`).
*   `POST /api/appointments` — Schedule an appointment (verifies doctor is active, auto-generates `TokenNumber`).
*   `GET /api/appointments/patient/{patientId}` — List all appointments for a patient.
*   `GET /api/appointments/doctor/{doctorId}` — List all appointments for a doctor.
*   `PUT /api/appointments/{appointmentId}` — Update appointment details.
*   `PATCH /api/appointments/<int:appointmentId>/cancel` — Cancel appointment (`ConsultationStatus = 'Cancelled'`).
*   `GET /api/billing` — List bills (supports optional filtering by `startDate` and `endDate`).
*   `POST /api/billing` — Generate consultation bill (auto-pulls consultation fee, calculates total amount).
*   `GET /api/billing/{appointmentId}` — Retrieve bill details by appointment ID.
*   `PUT /api/billing/{appointmentId}` — Update bill details.

### 🩺 Doctor Module
*   `POST /api/consultations` — Add consultation symptoms, diagnosis, and notes.
*   `GET /api/consultations/patient/{patientId}` — List consultation history by patient.
*   `GET /api/consultations/doctor/{doctorId}` — List consultation history by doctor.
*   `GET /api/consultations/history/appointment/{appointmentId}` — Get consultation by appointment ID.
*   `POST /api/prescriptions/medicine` — Prescribe medicines (supports single or bulk lists).
*   `PUT /api/prescriptions/medicine/{prescriptionId}` — Update a prescription entry.
*   `GET /api/prescriptions/medicine/appointment/{appointmentId}` — Get prescribed medicines for an appointment.
*   `GET /api/prescriptions/medicine/patient/{patientId}` — Get prescribed medicines by patient.
*   `GET /api/prescriptions/medicine/history/doctor/{doctorId}` — Get prescribed medicines by doctor.
*   `POST /api/prescriptions/labtest` — Prescribe lab tests (supports single or bulk lists).
*   `PUT /api/prescriptions/labtest/{prescriptionId}` — Update a lab test prescription.
*   `GET /api/prescriptions/labtest/appointment/{appointmentId}` — Get lab test prescriptions for an appointment.
*   `GET /api/prescriptions/labtest/patient/{patientId}` — Get lab test prescriptions by patient.

### 💊 Pharmacist Module
*   `GET /api/medicines` — List all active medicines.
*   `POST /api/medicines` — Create a new medicine (validates `ExpiryDate` is after `ManufacturingDate`).
*   `GET /api/medicines/{medicineId}` — Get medicine by ID.
*   `PUT /api/medicines/{medicineId}` — Update medicine details.
*   `PATCH /api/medicines/{medicineId}/deactivate` — Soft-deactivates medicine.
*   `GET /api/inventory/medicine` — List inventory stocks.
*   `POST /api/inventory/medicine` — Add stock configuration.
*   `GET /api/inventory/medicine/{medicineId}` — Get stock for a specific medicine.
*   `PUT /api/inventory/medicine/stock/{medicineStockId}` — Update stock quantity.
*   `PATCH /api/inventory/medicine/stock/{medicineStockId}/flag-low` — Flag inventory item as low stock.
*   `POST /api/inventory/medicine/dispense` — Custom dispense endpoint to subtract stock and auto-flag low quantities.

### 🧪 Lab Technician Module
*   `GET /api/labtests` — List all active lab tests.
*   `POST /api/labtests` — Add a new lab test.
*   `GET /api/labtests/{labTestId}` — Retrieve lab test details.
*   `PUT /api/labtests/{labTestId}` — Update lab test details.
*   `PATCH /api/labtests/{labTestId}/deactivate` — Soft-deactivates lab test.
*   `GET /api/labtests/results/appointment/{appointmentId}` — List prescribed lab tests and values for an appointment.
*   `GET /api/labtests/results` — List results (supports `startDate` and `endDate` range filtering).
*   `PUT /api/labtests/results/{labTestPrescriptionId}` — Record or update lab test results (`LabTestValue` and `Remarks`).
*   `PATCH /api/labtests/{labTestPrescriptionId}/deactivate` — Soft-deactivates prescription entry.
