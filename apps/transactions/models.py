from django.db import models
from apps.users.models import User

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('transfer', 'Transfer')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.amount})"
