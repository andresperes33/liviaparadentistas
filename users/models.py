from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Campos que o banco 'users' já possui ou que são seguros
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    # Novos campos como opcionais
    nome = models.CharField("nome", max_length=255, null=True, blank=True)
    telefone = models.CharField("telefone", max_length=20, null=True, blank=True)
    mensagens = models.IntegerField("mensagens", default=0)
    tem_plano = models.BooleanField("tem_plano", default=False)
    
    assinatura_status = models.CharField(max_length=50, default='inativa')
    kirvano_user_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "users" # O NOME REAL NO SEU BANCO DE DADOS! 🎯💎
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
