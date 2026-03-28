import random
import string
from django.db import models
from django.conf import settings

def generate_transaction_id():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(3))

class Transaction(models.Model):
    id = models.CharField(
        max_length=3,
        primary_key=True,
        editable=False
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    
    # Financial Mapping
    tipo = models.CharField("Tipo", max_length=20, null=True, blank=True)
    valor = models.DecimalField("Valor", max_digits=12, decimal_places=2, null=True, blank=True)
    descricao = models.TextField("Descrição", null=True, blank=True)
    categoria = models.CharField("Categoria", max_length=150, null=True, blank=True)
    data_transacao = models.DateField("Data da Transação", null=True, blank=True)
    status_pagamento = models.CharField("Status de Pagamento", max_length=50, null=True, blank=True)
    is_financial = models.BooleanField("É Transação Financeira?", default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "transactions"
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        
    def save(self, *args, **kwargs):
        if not self.id:
            # Generate ID and ensure uniqueness to avoid collision
            new_id = generate_transaction_id()
            while Transaction.objects.filter(id=new_id).exists():
                new_id = generate_transaction_id()
            self.id = new_id
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.id} - {self.user.username}"
