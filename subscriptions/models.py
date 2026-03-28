from django.db import models
from django.conf import settings
from django.utils import timezone

class Subscription(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="subscription"
    )
    active = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subscriptions"
        verbose_name = "Assinatura"
        verbose_name_plural = "Assinaturas"

    def is_valid(self) -> bool:
        """
        Check if the subscription is currently active and hasn't expired.
        """
        if not self.active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True

    def __str__(self):
        status = "Ativa" if self.is_valid() else "Inativa/Expirada"
        return f"Assinatura do {self.user.username} - {status}"


class KirvanoWebhookLog(models.Model):
    event_type = models.CharField(max_length=100, null=True, blank=True)
    payload = models.JSONField(null=True, blank=True)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "kirvano_webhook_logs"
        verbose_name = "Log Kirvano Webhook"
        verbose_name_plural = "Logs Kirvano Webhook"

    def __str__(self):
        return f"Kirvano Log {self.id} - {self.event_type}"
