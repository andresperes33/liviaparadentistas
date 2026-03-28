from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import MessageProcessingService
import logging

logger = logging.getLogger("django")

class WebhookReceiverView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        payload = request.data
        logger.info("Received Webhook Payload")
        
        try:
            # Em um cenário puramente guiado a eventos o handler de processamento seria movido pro Celery
            # Aqui rodamos synchronous a triagem (rápida) e apenas Áudio/Imagem em Celery.
            MessageProcessingService.handle_incoming_webhook(payload)
        except Exception as e:
            logger.error(f"Error handling webhook logic: {e}")
            
        # Evolution API necessita do status 200 rápido para não re-tentar várias vezes
        return Response({"status": "received"}, status=status.HTTP_200_OK)
