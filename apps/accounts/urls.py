from django.urls import path
from .views import TestProtectedView, CardListCreateView, DepositView, TransferView, BalanceView

urlpatterns = [
    path('test-auth/', TestProtectedView.as_view(), name='test_auth'),
    path('cards/', CardListCreateView.as_view(), name='cards'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('balance/', BalanceView.as_view(), name='balance'),
]
