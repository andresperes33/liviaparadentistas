from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # Organizando as colunas para ficarem idênticas ao exemplo do cliente
    list_display = (
        "id", 
        "created_at", 
        "descricao", 
        "categoria", 
        "valor", 
        "tipo", 
        "data", 
        "esta_pago", 
        "user", # Referência ao objeto User
        "identificador", # VP0
        "time" # Timestamp MS
    )
    
    list_filter = ("tipo", "categoria", "esta_pago", "data")
    search_fields = ("user__username", "identificador", "descricao", "categoria")
    readonly_fields = ("created_at", "time", "identificador")
    
    ordering = ("-created_at",)
