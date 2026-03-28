from django.contrib import admin
from .models import Subscription, KirvanoWebhookLog

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "active", "expires_at", "created_at")

@admin.register(KirvanoWebhookLog)
class KirvanoWebhookLogAdmin(admin.ModelAdmin):
    list_display = ("id", "event_type", "processed", "created_at")
