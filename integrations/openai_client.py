import os
from openai import OpenAI
import logging

logger = logging.getLogger("integrations")

class OpenAICore:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribes an audio file into text using OpenAI Whisper.
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise e

    def extract_text_from_image(self, image_url: str) -> str:
        """
        Extracts visible text from an image using OpenAI Vision model.
        """
        prompt = "Extraia apenas o texto visível da imagem enviada. Não adicione interpretações, descrições ou comentários. Retorne somente o texto puro exatamente como aparece na imagem."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url,
                                },
                            },
                        ],
                    }
                ],
                max_tokens=2048,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error extracting text from image: {str(e)}")
            raise e

openai_client = OpenAICore()
