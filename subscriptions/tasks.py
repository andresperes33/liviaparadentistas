from celery import shared_task
from .models import KirvanoWebhookLog
from users.models import User
from integrations.evolution_client import evolution_client
from messages.models import Message
from transactions.models import Transaction
from django.utils.dateparse import parse_datetime
import logging

logger = logging.getLogger("django")

@shared_task
def process_kirvano_event(log_id: int):
    try:
        log_entry = KirvanoWebhookLog.objects.get(id=log_id)
        payload = log_entry.payload
        event_type = payload.get("event_type")
        
        customer_email = payload.get("customer_email", "").strip().lower()
        customer_phone = payload.get("customer_phone", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        customer_name = payload.get("customer_name", "")
        plan_name = payload.get("plan_name", "")
        subscription_id = payload.get("subscription_id", "")
        
        next_billing_str = payload.get("next_billing_date")
        next_billing_date = parse_datetime(next_billing_str) if next_billing_str else None

        if event_type == "SALE_APPROVED":
            handle_sale_approved(customer_email, customer_phone, customer_name, plan_name, subscription_id, next_billing_date)
        elif event_type == "SUBSCRIPTION_RENEWED":
            handle_subscription_renewed(customer_email, next_billing_date)
        elif event_type == "SUBSCRIPTION_CANCELED":
            handle_subscription_canceled(customer_email)
        elif event_type == "SUBSCRIPTION_EXPIRED":
            handle_subscription_expired(customer_email)
        elif event_type == "PAYMENT_FAILED":
            handle_payment_failed(customer_email)
        else:
            logger.info(f"Unhandled Kirvano event_type: {event_type}")

        log_entry.processed = True
        log_entry.save()
        
    except Exception as e:
        logger.error(f"Error processing Kirvano Webhook log_id {log_id}: {e}")

def _send_and_log_evolution_msg(user: User, text: str):
    if not user.phone:
        logger.error(f"Cannot send Evolution API message, User {user.email} has no phone mapped.")
        return
        
    evolution_client.send_text(user.phone, text)
    transaction = Transaction.objects.create(user=user)
    Message.objects.create(
        user=user,
        transaction=transaction,
        message_type=Message.MessageType.TEXT,
        direction=Message.Direction.OUTBOUND,
        content=text
    )

def handle_sale_approved(email, phone, name, plan, sub_id, next_billing):
    user, created = User.objects.get_or_create(email=email, defaults={
        'phone': phone,
        'username': email.split("@")[0] + phone[-4:] if phone else email.split("@")[0],
    })
    
    if created:
        user.first_name = name
        
    user.tem_plano = True
    user.plano = plan
    user.assinatura_status = "ativa"
    user.proxima_cobranca = next_billing
    user.subscription_id = sub_id
    # Atualizar telefone caso estivesse nulo ou desatualizado pela Kirvano
    if phone and not user.phone:
        user.phone = phone
    user.save()
    
    logger.info(f"[Subscription] Acesso liberado para {email}")
    text = f"🎉 Obrigado pela sua compra!\n\nSeu acesso à Lívia já está liberado 🔑\n\nAgora você já pode enviar mensagens normalmente e utilizar sua assistente financeira para dentistas."
    _send_and_log_evolution_msg(user, text)

def handle_subscription_renewed(email, next_billing):
    try:
        user = User.objects.get(email=email)
        user.tem_plano = True
        user.assinatura_status = "ativa"
        user.proxima_cobranca = next_billing
        user.save()
        
        logger.info(f"[Subscription] Assinatura renovada: {email}")
        text = "✅ Sua assinatura da Lívia foi renovada com sucesso.\n\nSeu acesso continua ativo normalmente."
        _send_and_log_evolution_msg(user, text)
    except User.DoesNotExist:
        logger.error(f"Renewed for unknown email: {email}")

def handle_subscription_canceled(email):
    try:
        user = User.objects.get(email=email)
        user.tem_plano = False
        user.assinatura_status = "cancelada"
        user.save()
        
        logger.info(f"[Subscription] Assinatura cancelada: {email}")
        link = f"https://liviaparadentistas.com.br/renovar/{user.username}"
        text = f"Sua assinatura da Lívia foi cancelada.\n\nVocê ainda pode reativar seu acesso quando quiser através do link abaixo:\n\n{link}"
        _send_and_log_evolution_msg(user, text)
    except User.DoesNotExist:
        logger.error(f"Canceled for unknown email: {email}")

def handle_subscription_expired(email):
    try:
        user = User.objects.get(email=email)
        user.tem_plano = False
        user.assinatura_status = "expirada"
        user.save()
        
        logger.info(f"[Subscription] Assinatura expirada: {email}")
        link = f"https://liviaparadentistas.com.br/renovar/{user.username}"
        text = f"Seu acesso à Lívia expirou.\n\nPara voltar a utilizar a plataforma, renove sua assinatura no link abaixo:\n\n{link}"
        _send_and_log_evolution_msg(user, text)
    except User.DoesNotExist:
        logger.error(f"Expired for unknown email: {email}")

def handle_payment_failed(email):
    try:
        user = User.objects.get(email=email)
        user.assinatura_status = "pagamento_falhou"
        user.save()
        
        logger.info(f"[Subscription] Pagamento falhou: {email}")
        link = f"https://liviaparadentistas.com.br/pagamento/{user.username}"
        text = f"⚠️ Não conseguimos processar o pagamento da sua assinatura da Lívia.\n\nVerifique sua forma de pagamento e tente novamente através do link abaixo:\n\n{link}"
        _send_and_log_evolution_msg(user, text)
    except User.DoesNotExist:
        logger.error(f"Payment failed for unknown email: {email}")
