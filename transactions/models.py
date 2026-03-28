import random
import string
import time
from django.db import models
from django.conf import settings

def generate_identificador():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(3))

class Transaction(models.Model):
    # id (AutoField)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions", verbose_name="user_id")
    
    # Campos com verbose_name exatamente como solicitado
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    descricao = models.TextField(verbose_name="descricao", null=True, blank=True)
    categoria = models.CharField(verbose_name="categoria", max_length=150, null=True, blank=True)
    valor = models.DecimalField(verbose_name="valor", max_digits=12, decimal_places=2, null=True, blank=True)
    tipo = models.CharField(verbose_name="tipo", max_length=20, null=True, blank=True)
    data = models.DateField(verbose_name="data", null=True, blank=True)
    esta_pago = models.BooleanField(verbose_name="esta_pago", default=False)
    identificador = models.CharField(verbose_name="identificador", max_length=10, null=True, blank=True)
    time = models.BigIntegerField(verbose_name="time", null=True, blank=True)
    
    class Meta:
        db_table = "transactions"
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        
    def save(self, *args, **kwargs):
        if not self.identificador:
            self.identificador = generate_identificador()
        if not self.time:
            self.time = int(time.time() * 1000)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.id} - {self.identificador} - {self.user.username}"
