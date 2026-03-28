from django.urls import path
from .views import KirvanoWebhookView

urlpatterns = [
    path('webhooks/kirvano/', KirvanoWebhookView.as_view(), name='kirvano_webhook'),
]
