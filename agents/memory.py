import json
import logging
import redis
from django.conf import settings

logger = logging.getLogger("django")

try:
    redis_url = getattr(settings, "REDIS_URL", "redis://localhost:6379/0")
    redis_client = redis.StrictRedis.from_url(redis_url, decode_responses=True)
except Exception as e:
    logger.error(f"Não foi possível conectar ao Redis: {e}")
    redis_client = None

class ConversationMemory:
    """Gerencia o histórico de conversa no Redis para manter contexto."""
    
    EXPIRATION_SECONDS = 86400  # 24 horas

    @staticmethod
    def get_key(telefone: str) -> str:
        return f"livia:chat_history:{telefone}"

    @staticmethod
    def get_history(telefone: str) -> list:
        """Retorna o histórico do Redis."""
        if not redis_client:
            return []
        key = ConversationMemory.get_key(telefone)
        data = redis_client.get(key)
        return json.loads(data) if data else []

    @staticmethod
    def add_message(telefone: str, role: str, content: str):
        """Adiciona uma mensagem ao histórico no Redis."""
        if not redis_client:
            return
        key = ConversationMemory.get_key(telefone)
        history = ConversationMemory.get_history(telefone)
        history.append({"role": role, "content": content})
        
        # Mantém apenas as últimas 15 mensagens para contexto
        redis_client.setex(key, ConversationMemory.EXPIRATION_SECONDS, json.dumps(history[-15:]))

    @staticmethod
    def clear_history(telefone: str):
        """Apaga o histórico do usuário."""
        if redis_client:
            redis_client.delete(ConversationMemory.get_key(telefone))
