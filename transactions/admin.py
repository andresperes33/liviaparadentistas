from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # Agora que mudamos o verbose_name no models.py, podemos usar os nomes diretos
    list_display = (
        "id", 
        "created_at", 
        "descricao", 
        "categoria", 
        "valor", 
        "tipo", 
        "data", 
        "esta_pago", 
        "user_id", 
        "identificador", 
        "time"
    )
    
    list_filter = ("tipo", "categoria", "esta_pago", "data")
    search_fields = ("user__username", "identificador", "descricao", "categoria")
    readonly_fields = ("created_at", "time", "identificador")
    
    ordering = ("-created_at",)
