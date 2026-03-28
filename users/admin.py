from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # Metodos para forçar nomes em minúsculo no cabeçalho
    def _id(self, obj): return obj.id
    _id.short_description = 'id'
    
    def _created_at(self, obj): return obj.created_at
    _created_at.short_description = 'created_at'
    
    def _nome(self, obj): return obj.nome
    _nome.short_description = 'nome'
    
    def _telefone(self, obj): return obj.telefone
    _telefone.short_description = 'telefone'
    
    def _email(self, obj): return obj.email
    _email.short_description = 'email'
    
    def _mensagens(self, obj): return obj.mensagens
    _mensagens.short_description = 'mensagens'
    
    def _tem_plano(self, obj): return obj.tem_plano
    _tem_plano.short_description = 'tem_plano'
    _tem_plano.boolean = True

    # Lista de exibição oficial iguaal ao seu print
    list_display = (
        '_id', 
        '_created_at', 
        '_nome', 
        '_telefone', 
        '_email', 
        '_mensagens', 
        '_tem_plano'
    )
    
    list_filter = ('tem_plano', 'assinatura_status')
    search_fields = ('telefone', 'nome', 'email')
    ordering = ('-created_at',)
    
    # Campos que podem ser editados no formulário
    fieldsets = (
        (None, {'fields': ('telefone', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'email')}),
        ('Status', {'fields': ('tem_plano', 'mensagens', 'assinatura_status', 'kirvano_user_id')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
