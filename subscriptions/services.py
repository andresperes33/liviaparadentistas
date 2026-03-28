from subscriptions.models import Subscription
from users.models import User
import logging
from django.utils import timezone

logger = logging.getLogger("django")

class SubscriptionService:
    @staticmethod
    def check_user_access(user: User) -> bool:
        """
        Returns True if the user has an active, non-expired subscription.
        Agora validado através do espelho de assinatura nativo no usuário via Kirvano.
        """
        if user.tem_plano and user.assinatura_status == "ativa":
            if user.proxima_cobranca and user.proxima_cobranca < timezone.now():
                return False
            return True
        return False
            
    @staticmethod
    def get_renewal_link(user: User) -> str:
        return f"https://liviaparadentistas.com.br/renovar/{user.username}"
        
    @staticmethod
    def get_signup_link(phone: str) -> str:
        return f"https://liviaparadentistas.com.br/assinar?phone={phone}"
