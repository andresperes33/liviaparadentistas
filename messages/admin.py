from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("direction", "message_type", "user", "transaction", "created_at")
    list_filter = ("direction", "message_type")
    search_fields = ("user__username", "user__phone", "content")
    readonly_fields = ("created_at",)
