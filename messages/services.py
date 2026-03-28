import logging
from messages.models import Message
from users.services import UserService
from subscriptions.services import SubscriptionService
from transactions.models import Transaction
from integrations.evolution_client import evolution_client
from messages.tasks import process_audio_message, process_image_message
from agents.bot import LiviaAgentService
from agents.router_bot import LiviaRouterBot

logger = logging.getLogger("django")

class MessageProcessingService:
    @staticmethod
    def handle_incoming_webhook(payload: dict):
        try:
            data = payload.get("data", {})
            if "messages" in data:
                message_item = data["messages"][0]
            else:
                message_item = data
                
            from_me = message_item.get("key", {}).get("fromMe", False)
            logger.info(f"Message fromMe: {from_me} | Sender: {message_item.get('key', {}).get('remoteJid')}")
            
            if from_me:
                logger.info("Ignoring message because it is fromMe")
                return

            remote_jid = message_item.get("key", {}).get("remoteJid", "")
            if not remote_jid or "@g.us" in remote_jid:
                return
                
            sender = remote_jid.split("@")[0]
            
            # Prevenir loop caso a Evolution API repasse a própria mensagem da Livia
            # if sender == "553898781988":
            #     return
                
            msg_obj = message_item.get("message", {})
            if not msg_obj:
                return
                
            msg_type_str = list(msg_obj.keys())[0] if msg_obj else "unknown"
            logger.info(f"Message Type: {msg_type_str} | Content keys: {list(msg_obj.keys()) if msg_obj else 'None'}")
            
            content = ""
            if "conversation" in msg_obj:
                content = msg_obj.get("conversation")
            elif "extendedTextMessage" in msg_obj:
                content = msg_obj.get("extendedTextMessage", {}).get("text", "")
            elif "messageContextInfo" in msg_obj and "conversation" in msg_obj:
                content = msg_obj.get("conversation")

            user = UserService.get_user_by_phone(sender)
            
            # 1. Usuário não existe -> Mensagem Estática de Boas-vindas e Link Kirvano
            if not user:
                welcome_msg = (
                    "Olá! 👋\n"
                    "Eu sou a Lívia, sua assistente financeira 🧡\n\n"
                    "Estou aqui para ajudar você, dentista, a organizar as finanças do seu consultório de forma simples, prática e estratégica 💰🦷\n\n"
                    "Chega de misturar contas, perder o controle do caixa ou ficar na dúvida sobre para onde está indo o seu dinheiro.\n"
                    "Vamos colocar sua vida financeira nos trilhos e dar mais tranquilidade para você focar no que realmente importa: seus pacientes e o crescimento do seu consultório 🚀\n\n"
                    "👉 Para começar, faça seu cadastro por aqui:\n"
                    "https://pay.kirvano.com/e45b2cc2-243c-43b3-9071-6f8c226450df"
                )
                evolution_client.send_text(sender, welcome_msg)
                return

            # 2. Usuário existe mas está inativo (Limite atingido ou Expirado) -> Mensagem Estática de Upgrade
            if not SubscriptionService.check_user_access(user):
                limit_msg = (
                    "⚠️ Atenção! ⚠️ Detectei que você atingiu o limite de transações do seu plano atual. 😔\n"
                    "Pra continuar usando a Lívia sem interrupções, recomendo atualizar seu plano para um que atenda melhor às suas necessidades. 🚀💳\n"
                    "Acesse o link abaixo pra conferir as opções e fazer o upgrade:\n"
                    "https://pay.kirvano.com/e45b2cc2-243c-43b3-9071-6f8c226450df"
                )
                evolution_client.send_text(sender, limit_msg)
                
                transaction = Transaction.objects.create(user=user)
                Message.objects.create(user=user, transaction=transaction, message_type=Message.MessageType.TEXT, direction=Message.Direction.INBOUND, content=content)
                Message.objects.create(user=user, transaction=transaction, message_type=Message.MessageType.TEXT, direction=Message.Direction.OUTBOUND, content=limit_msg)
                return
                
            # 3. Usuário Válido -> Fluxo de Livia Contábil
            transaction = Transaction.objects.create(user=user)
            
            if "conversation" in msg_type_str or "extendedTextMessage" in msg_type_str:
                reply_text = LiviaRouterBot.process_message(user, content, transaction)
                
                Message.objects.create(user=user, transaction=transaction, message_type=Message.MessageType.TEXT, direction=Message.Direction.INBOUND, content=content)
                Message.objects.create(user=user, transaction=transaction, message_type=Message.MessageType.TEXT, direction=Message.Direction.OUTBOUND, content=reply_text)
                evolution_client.send_text(user.telefone, reply_text)
                
            elif "audioMessage" in msg_type_str:
                media_url = msg_obj.get("audioMessage", {}).get("url", "")
                msg = Message.objects.create(
                    user=user, transaction=transaction, message_type=Message.MessageType.AUDIO, 
                    direction=Message.Direction.INBOUND, content="", media_url=media_url)
                process_audio_message.delay(msg.id, sender)
            elif "imageMessage" in msg_type_str:
                image_url = msg_obj.get("imageMessage", {}).get("url", "https://example.com/uploaded.jpg")
                msg = Message.objects.create(
                    user=user, transaction=transaction, message_type=Message.MessageType.IMAGE, 
                    direction=Message.Direction.INBOUND, content="", media_url=image_url)
                process_image_message.delay(msg.id, sender, image_url)
            else:
                logger.info(f"Mensagem de tipo desconhecido/ignorado ({msg_type_str}) de {sender}")
                
        except Exception as e:
            logger.error(f"Erro brutal ao processar webhook genérico: {e}")
