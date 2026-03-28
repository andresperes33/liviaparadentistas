from django.contrib import admin
from .models import Subscription, KirvanoWebhookLog

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "active", "expires_at", "is_valid")
    list_filter = ("active",)
    search_fields = ("user__username", "user__phone")

@admin.register(KirvanoWebhookLog)
class KirvanoWebhookLogAdmin(admin.ModelAdmin):
    list_display = ("id", "event_type", "processed", "created_at")
    list_filter = ("event_type", "processed")
    readonly_fields = ("created_at",)
