from django.contrib import admin
from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # Exibir apenas ID e E-mail (que já existem no banco por padrão)
    list_display = ('id', 'email')
    
    # Comentei tudo o que depende dos campos novos
    # list_filter = ('tem_plano',)
    # search_fields = ('telefone',)
