# Migration robusta com RunSQL + IF NOT EXISTS
# Garante que as colunas são criadas mesmo que o historico de migrations esteja inconsistente

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_assinatura_status_user_plano_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS nome VARCHAR(255);",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS telefone VARCHAR(20);",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS mensagens INTEGER NOT NULL DEFAULT 0;",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS kirvano_user_id VARCHAR(100);",
            ],
            reverse_sql=[
                "ALTER TABLE users DROP COLUMN IF EXISTS nome;",
                "ALTER TABLE users DROP COLUMN IF EXISTS telefone;",
                "ALTER TABLE users DROP COLUMN IF EXISTS mensagens;",
                "ALTER TABLE users DROP COLUMN IF EXISTS kirvano_user_id;",
            ]
        ),
    ]
