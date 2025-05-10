from django.db import models
from apps.users.models import User
from apps.accounts.models import Card


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('transfer', 'Transfer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, related_name='sent_transactions', blank=True)
    to_card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, related_name='received_transactions', blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.telegram_id} - {self.transaction_type} - {self.amount}"
