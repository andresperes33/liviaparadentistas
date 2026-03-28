from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from users.models import User
from subscriptions.models import Subscription
from subscriptions.services import SubscriptionService

class SubscriptionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", phone="123")
        
    def test_active_subscription(self):
        Subscription.objects.create(
            user=self.user, 
            active=True, 
            expires_at=timezone.now() + timedelta(days=30)
        )
        self.assertTrue(SubscriptionService.check_user_access(self.user))
        
    def test_expired_subscription(self):
        Subscription.objects.create(
            user=self.user, 
            active=True, 
            expires_at=timezone.now() - timedelta(days=1)
        )
        self.assertFalse(SubscriptionService.check_user_access(self.user))
        
    def test_inactive_subscription(self):
        Subscription.objects.create(
            user=self.user, 
            active=False, 
            expires_at=timezone.now() + timedelta(days=30)
        )
        self.assertFalse(SubscriptionService.check_user_access(self.user))
