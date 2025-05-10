from django.db import models
from apps.users.models import User


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=16, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_number} - {self.user.telegram_id}"
