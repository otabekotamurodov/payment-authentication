from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_transactions, name='get_transactions'),
    path("request-transfer/", views.request_transfer, name="request_transfer"),
    path("confirm-transfer/", views.confirm_transfer, name="confirm_transfer"),

]

