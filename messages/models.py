from django.db import models
from django.conf import settings
from transactions.models import Transaction

class Message(models.Model):
    class MessageType(models.TextChoices):
        TEXT = 'TEXT', 'Texto'
        AUDIO = 'AUDIO', 'Áudio'
        IMAGE = 'IMAGE', 'Imagem'
        
    class Direction(models.TextChoices):
        INBOUND = 'INBOUND', 'Recebida'
        OUTBOUND = 'OUTBOUND', 'Enviada'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages")
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="messages", null=True, blank=True)
    
    message_type = models.CharField(max_length=10, choices=MessageType.choices, default=MessageType.TEXT)
    direction = models.CharField(max_length=10, choices=Direction.choices, default=Direction.INBOUND)
    
    content = models.TextField() 
    media_url = models.URLField(max_length=500, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messages"
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.direction} - {self.message_type} - {self.user.username}"
