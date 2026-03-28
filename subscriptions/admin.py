from django.contrib import admin
from .models import Subscription, KirvanoWebhookLog

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'next_billing_date', 'plan_name')
    list_filter = ("active",)
    search_fields = ("user__username", "user__telefone")

@admin.register(KirvanoWebhookLog)
class KirvanoWebhookLogAdmin(admin.ModelAdmin):
    list_display = ("id", "event_type", "processed", "created_at")
    list_filter = ("event_type", "processed")
    readonly_fields = ("created_at",)
