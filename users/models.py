import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('O Username é obrigatório')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractUser):
    # Voltando ao padrão Django temporariamente para destravar o servidor
    username = models.CharField(max_length=150, unique=True)
    
    # Novos nomes técnicos (vão funcionar após o deploy/migrate)
    nome = models.CharField("nome", max_length=255, null=True, blank=True)
    telefone = models.CharField("telefone", max_length=20, null=True, blank=True)
    email = models.EmailField("email", null=True, blank=True)
    
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    mensagens = models.IntegerField("mensagens", default=0)
    tem_plano = models.BooleanField("tem_plano", default=False)
    
    kirvano_user_id = models.CharField(max_length=100, null=True, blank=True)
    assinatura_status = models.CharField(max_length=50, default='inativa')

    objects = UserManager()

    # Login temporário por username enquanto o banco atualiza
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.username} - {self.nome or 'Sem Nome'}"
