from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.auth_module.views import LoginView, LogoutView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
