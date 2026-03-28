import redis
import json
import os
import logging

logger = logging.getLogger("django")

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
try:
    redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_client = None

class ConversationMemory:
    """Manager to keep a sliding window of conversation in Redis for 24 hours."""
    EXPIRATION_SECONDS = 86400 # 24 hours
    
    @staticmethod
    def get_key(phone: str) -> str:
        return f"livia:chat_history:{phone}"
        
    @staticmethod
    def get_history(phone: str) -> list:
        if not redis_client:
            return []
        key = ConversationMemory.get_key(phone)
        data = redis_client.get(key)
        if data:
            parsed = json.loads(data)
            return parsed if isinstance(parsed, list) else []
        return []

    @staticmethod
    def add_message(phone: str, role: str, content: str):
        if not redis_client:
            return
        key = ConversationMemory.get_key(phone)
        history = ConversationMemory.get_history(phone)
        
        history.append({"role": role, "content": content})
        
        # Manter limitadas as ultimas 20 mensagens (10 idas e voltas contextuais)
        if len(history) > 20:
            history = history[-20:]
            
        redis_client.setex(key, ConversationMemory.EXPIRATION_SECONDS, json.dumps(history))
        
    @staticmethod
    def clear_history(phone: str):
        if redis_client:
            redis_client.delete(ConversationMemory.get_key(phone))
