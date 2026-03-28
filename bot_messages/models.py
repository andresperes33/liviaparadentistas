from django.db import models
from django.conf import settings
from transactions.models import Transaction

class Message(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    )
    
    TYPE_CHOICES = (
        ('text', 'Text'),
        ('audio', 'Audio'),
        ('image', 'Image'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bot_messages")
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="bot_messages", null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    message_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='text')
    content = models.TextField()
    media_url = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bot_messages" # Corrigido para o novo nome!
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"

    def __str__(self):
        return f"{self.user.username} - {self.role}: {self.content[:30]}..."
