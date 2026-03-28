from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import KirvanoWebhookLog
from .tasks import process_kirvano_event
import logging

logger = logging.getLogger("django")

class KirvanoWebhookView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        payload = request.data
        event_type = payload.get("event_type", "UNKNOWN")
        
        logger.info(f"[KirvanoWebhook] Evento recebido: {event_type} | Email: {payload.get('customer_email', 'N/A')}")
        
        try:
            log_entry = KirvanoWebhookLog.objects.create(
                event_type=event_type,
                payload=payload
            )
            process_kirvano_event.delay(log_entry.id)
        except Exception as e:
            logger.error(f"Failed to log Kirvano Webhook: {e}")
            
        return Response({"status": "received"}, status=status.HTTP_200_OK)
