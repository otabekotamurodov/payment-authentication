from django.urls import path
from .views import begin_registration, finish_registration
from .views import begin_authentication, finish_authentication

urlpatterns = [
    path('begin-registration/', begin_registration),
    path('finish-registration/', finish_registration),
    path("begin-authentication/", begin_authentication),
    path("finish-authentication/", finish_authentication),
]
