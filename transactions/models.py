import random
import string
import time
from django.db import models
from django.conf import settings

def generate_identificador():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(3))

class Transaction(models.Model):
    # id padrão AutoField (int8) será criado automaticamente pelo Django
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    
    # Campos alinhados com o exemplo do cliente
    identificador = models.CharField("Identificador", max_length=10, null=True, blank=True)
    descricao = models.TextField("Descrição", null=True, blank=True)
    categoria = models.CharField("Categoria", max_length=150, null=True, blank=True)
    valor = models.DecimalField("Valor", max_digits=12, decimal_places=2, null=True, blank=True)
    tipo = models.CharField("Tipo", max_length=20, null=True, blank=True)
    data = models.DateField("Data", null=True, blank=True)
    esta_pago = models.BooleanField("Está Pago?", default=False)
    time = models.BigIntegerField("Time (MS)", null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
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
