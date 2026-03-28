from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ("WhatsApp & Kirvano", {"fields": ("phone", "tem_plano", "plano", "assinatura_status", "proxima_cobranca", "subscription_id")}),
    )
    list_display = ("username", "phone", "email", "assinatura_status", "tem_plano")
    search_fields = ("username", "phone", "email")
    list_filter = ("assinatura_status", "tem_plano")
