from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Campos básicos que o banco já deve ter ou que são seguros
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    # Novos campos como opcionais (para não travar se a migração não rodou)
    nome = models.CharField(max_length=255, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    mensagens = models.IntegerField(default=0)
    tem_plano = models.BooleanField(default=False)
    
    assinatura_status = models.CharField(max_length=50, default='inativa')

    class Meta:
        db_table = "users_user" # Forçando o nome padrão do Django
