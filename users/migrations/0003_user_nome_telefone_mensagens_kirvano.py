# Generated manually on 2026-03-28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_assinatura_status_user_plano_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nome',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='nome'),
        ),
        migrations.AddField(
            model_name='user',
            name='telefone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='telefone'),
        ),
        migrations.AddField(
            model_name='user',
            name='mensagens',
            field=models.IntegerField(default=0, verbose_name='mensagens'),
        ),
        migrations.AddField(
            model_name='user',
            name='kirvano_user_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
