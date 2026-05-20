from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.auth_module.urls')),
    path('api/', include('apps.admin_module.urls')),
    path('api/', include('apps.receptionist.urls')),
    path('api/', include('apps.doctor.urls')),
    path('api/', include('apps.pharmacist.urls')),
    path('api/', include('apps.lab_technician.urls')),
]
