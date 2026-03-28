from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # Usando os nomes corretos do modelo (role em vez de direction)
    list_display = ("role", "message_type", "user", "transaction", "created_at")
    list_filter = ("role", "message_type")
    
    # Usando telefone em vez de phone!
    search_fields = ("user__username", "user__telefone", "content")
    readonly_fields = ("created_at",)
