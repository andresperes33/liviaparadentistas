import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, telefone, password=None, **extra_fields):
        if not telefone:
            raise ValueError('O Telefone é obrigatório')
        user = self.model(telefone=telefone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telefone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(telefone, password, **extra_fields)

class User(AbstractUser):
    # Removendo campos padrão que não estão no print do cliente para o Admin, 
    # mas mantendo na estrutura para compatibilidade com Django
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    
    # Novos nomes técnicos solicitados
    nome = models.CharField("nome", max_length=255, null=True, blank=True)
    telefone = models.CharField("telefone", max_length=20, unique=True)
    email = models.EmailField("email", null=True, blank=True)
    
    # Campos que estavam no seu print
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    mensagens = models.IntegerField("mensagens", default=0)
    tem_plano = models.BooleanField("tem_plano", default=False)
    
    # Campo para compatibilidade com Kirvano (pode ficar oculto no Admin)
    kirvano_user_id = models.CharField(max_length=100, null=True, blank=True)
    assinatura_status = models.CharField(max_length=50, default='inativa')

    objects = UserManager()

    USERNAME_FIELD = 'telefone'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.telefone} - {self.nome or 'Sem Nome'}"
