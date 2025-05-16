from django.urls import path
from apps.users.views import generate_code, verify_code,refresh_token

urlpatterns = [
    path('auth/generate-code/', generate_code, name='generate_code'),
    path('auth/verify-code/', verify_code, name='verify_code'),
    path('token/refresh/', refresh_token, name='refresh_token'),
]
