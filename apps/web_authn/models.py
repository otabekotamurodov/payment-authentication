from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class WebAuthnCredential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credential_id = models.TextField()
    public_key = models.TextField()
    sign_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
