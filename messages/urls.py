from django.urls import path
from .views import WebhookReceiverView

urlpatterns = [
    path('webhook/evolution/', WebhookReceiverView.as_view(), name='evolution_webhook'),
]
