from django.contrib import admin
from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # Metodos robustos: Verificam se o campo existe antes de exibir
    def _id(self, obj): return obj.id
    _id.short_description = 'id'
    
    def _created_at(self, obj): 
        return getattr(obj, 'created_at', '---')
    _created_at.short_description = 'created_at'
    
    def _nome(self, obj): 
        return getattr(obj, 'nome', '---')
    _nome.short_description = 'nome'
    
    def _telefone(self, obj): 
        return getattr(obj, 'telefone', '---')
    _telefone.short_description = 'telefone'
    
    def _email(self, obj): 
        return getattr(obj, 'email', '---')
    _email.short_description = 'email'
    
    def _mensagens(self, obj): 
        return getattr(obj, 'mensagens', 0)
    _mensagens.short_description = 'mensagens'
    
    def _tem_plano(self, obj): 
        return getattr(obj, 'tem_plano', False)
    _tem_plano.short_description = 'tem_plano'
    _tem_plano.boolean = True

    # Lista de exibição oficial
    list_display = (
        '_id', 
        '_created_at', 
        '_nome', 
        '_telefone', 
        '_email', 
        '_mensagens', 
        '_tem_plano'
    )
    
    # Filtros e Buscas simplificados para evitar erro 500 antes da migração
    search_fields = ('email',) # Busca apenas por email por enquanto
    
    # Campos que podem ser editados no formulário
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'email', 'telefone')}),
        ('Status', {'fields': ('tem_plano', 'mensagens', 'assinatura_status')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
