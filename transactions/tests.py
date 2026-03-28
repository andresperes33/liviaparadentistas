from django.test import TestCase
from users.models import User
from transactions.models import Transaction

class TransactionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="dentist_tester", phone="1234")

    def test_transaction_id_generation(self):
        t1 = Transaction.objects.create(user=self.user)
        self.assertEqual(len(t1.id), 3)
        self.assertTrue(t1.id.isalnum())
        
        t2 = Transaction.objects.create(user=self.user)
        self.assertNotEqual(t1.id, t2.id)

    def test_transaction_id_uniqueness(self):
        transactions = [Transaction.objects.create(user=self.user) for _ in range(50)]
        ids = set(t.id for t in transactions)
        self.assertEqual(len(transactions), len(ids))
