import os
import requests
import logging

logger = logging.getLogger("integrations")

class EvolutionAPIClient:
    def __init__(self):
        self.base_url = os.getenv("EVOLUTION_API_URL", "http://localhost:8080").rstrip('/')
        self.token = os.getenv("EVOLUTION_API_TOKEN", "")
        self.headers = {
            "apikey": self.token,
            "Content-Type": "application/json"
        }
        self.instance_name = os.getenv("EVOLUTION_INSTANCE_NAME", "livia")
        
    def _post(self, endpoint: str, payload: dict):
        url = f"{self.base_url}/message/{endpoint}/{self.instance_name}"
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=15)
            response.raise_for_status()
            logger.info(f"Evolution API success: {endpoint} to {payload.get('number')}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Evolution API Error on {endpoint}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response content: {e.response.text}")
            return None

    def send_text(self, number: str, text: str):
        payload = {
            "number": number,
            "options": {
                "delay": 1200,
                "presence": "composing"
            },
            "textMessage": {
                "text": text
            }
        }
        return self._post("sendText", payload)

evolution_client = EvolutionAPIClient()
