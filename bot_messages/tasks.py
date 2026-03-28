from celery import shared_task
from integrations.openai_client import openai_client
from integrations.evolution_client import evolution_client
from bot_messages.models import Message
import logging

logger = logging.getLogger("django")

@shared_task
def process_audio_message(message_id: int, user_phone: str):
    try:
        msg = Message.objects.get(id=message_id)
        
        # Aqui, idealmente baixeríamos o arquivo de áudio da Evolution API
        # e passaríamos o caminho físico para o `openai_client.transcribe_audio`.
        # Transcrição simulada para compor a lógica base (presumindo sucesso no download):
        
        # audio_path = download_audio_from_evolution(...)
        # transcript = openai_client.transcribe_audio(audio_path)
        
        transcript = "[Simulação OCR/Transcrição] Audio Text"
        msg.content = transcript
        msg.save()
        
        reply_text = f"✔️ Áudio processado sob Transação: {msg.transaction.id}\n\nTranscrição:\n{transcript}"
        evolution_client.send_text(msg.user.phone, reply_text)
        
        Message.objects.create(
            user=msg.user,
            transaction=msg.transaction,
            message_type=Message.MessageType.TEXT,
            direction=Message.Direction.OUTBOUND,
            content=reply_text
        )
        
    except Exception as e:
        logger.error(f"Error processing audio for ID {message_id}: {e}")
        evolution_client.send_text(user_phone, "Ocorreu um erro ao processar sua mensagem. Tente novamente em alguns instantes.")

@shared_task
def process_image_message(message_id: int, user_phone: str, image_url: str):
    try:
        msg = Message.objects.get(id=message_id)
        
        # Extract text using Vision API
        # text = openai_client.extract_text_from_image(image_url)
        text = "[Simulação OCR] Image Text"
        msg.content = text
        msg.save()
        
        reply_text = f"✔️ Imagem processada sob Transação: {msg.transaction.id}\n\nTexto Extraído:\n{text}"
        evolution_client.send_text(msg.user.phone, reply_text)
        
        Message.objects.create(
            user=msg.user,
            transaction=msg.transaction,
            message_type=Message.MessageType.TEXT,
            direction=Message.Direction.OUTBOUND,
            content=reply_text
        )
        
    except Exception as e:
        logger.error(f"Error processing image for ID {message_id}: {e}")
        evolution_client.send_text(user_phone, "Ocorreu um erro ao processar sua mensagem. Tente novamente em alguns instantes.")
