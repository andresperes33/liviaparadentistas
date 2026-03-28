from users.models import User
import logging

logger = logging.getLogger("django")

class UserService:
    @staticmethod
    def get_user_by_phone(phone: str) -> User | None:
        """
        Returns a User by phone number or None if it doesn't exist.
        """
        try:
            return User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None
