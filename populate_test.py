import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from transactions.models import Transaction
from users.models import User

def populate():
    # Pega o primeiro usuário do banco para associar a transação
    user = User.objects.first()
    if not user:
        print("❌ Nenhum usuário encontrado no sistema!")
        return
        
    print(f"✅ Criando transação teste para o usuário: {user.username}")
    
    t = Transaction.objects.create(
        user=user,
        descricao="atendimento do dia",
        categoria="clinica ideal",
        valor=400.00,
        tipo="Receita",
        data=datetime.date(2026, 3, 3),
        esta_pago=False,
        identificador="VP0"
    )
    
    print(f"🎉 Transação criada com sucesso! ID: {t.id}")

if __name__ == "__main__":
    populate()
