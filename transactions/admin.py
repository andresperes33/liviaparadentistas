from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "tipo", "valor", "categoria", "data_transacao", "is_financial")
    list_filter = ("tipo", "categoria", "is_financial")
    search_fields = ("user__username", "user__phone", "descricao")
    readonly_fields = ("created_at",)
