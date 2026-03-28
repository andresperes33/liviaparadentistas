from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model for Livia Agents users (Dentists).
    Uses phone as an important identification field since WhatsApp is the main channel.
    """
    phone = models.CharField("Telefone", max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField("E-mail", unique=True, null=True, blank=True)
    
    # Campos da assinatura integrados à Kirvano
    tem_plano = models.BooleanField(default=False)
    plano = models.CharField("Plano", max_length=150, null=True, blank=True)
    assinatura_status = models.CharField("Status da Assinatura", max_length=50, null=True, blank=True)
    proxima_cobranca = models.DateTimeField("Próxima Cobrança", null=True, blank=True)
    subscription_id = models.CharField("Subscription ID Kirvano", max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = "users"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        
    def __str__(self):
        return f"{self.username} - {self.phone}"
