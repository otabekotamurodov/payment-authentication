from django.urls import path
from apps.users.views import generate_code, verify_code

urlpatterns = [
    path('auth/generate-code/', generate_code, name='generate_code'),
    path('auth/verify-code/', verify_code, name='verify_code'),
]
