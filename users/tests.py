from django.test import TestCase
from users.models import User
from users.services import UserService

class UserServiceTest(TestCase):
    def test_get_user_by_phone(self):
        User.objects.create(username="test_user", phone="5511999999999")
        
        user = UserService.get_user_by_phone("5511999999999")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "test_user")
        
        none_user = UserService.get_user_by_phone("000")
        self.assertIsNone(none_user)
