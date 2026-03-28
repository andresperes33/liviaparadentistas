from django.contrib import admin
from .models import Subscription, KirvanoWebhookLog

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "next_billing_date")

@admin.register(KirvanoWebhookLog)
class KirvanoWebhookLogAdmin(admin.ModelAdmin):
    list_display = ("id", "event_type", "status", "created_at")
