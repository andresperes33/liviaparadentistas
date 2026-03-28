from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # Métodos para forçar nomes em MAIÚSCULO (igual à tabela de usuários)
    def _id(self, obj): return obj.id
    _id.short_description = 'ID'
    
    def _created_at(self, obj): return obj.created_at
    _created_at.short_description = 'CREATED_AT'
    
    def _descricao(self, obj): return obj.descricao
    _descricao.short_description = 'DESCRIÇÃO'
    
    def _categoria(self, obj): return obj.categoria
    _categoria.short_description = 'CATEGORIA'
    
    def _valor(self, obj): return obj.valor
    _valor.short_description = 'VALOR'
    
    def _tipo(self, obj): return obj.tipo
    _tipo.short_description = 'TIPO'
    
    def _data(self, obj): return obj.data
    _data.short_description = 'DATA'
    
    def _esta_pago(self, obj): return obj.esta_pago
    _esta_pago.short_description = 'ESTA_PAGO'
    _esta_pago.boolean = True
    
    def _user_id(self, obj): return obj.user.id if obj.user else None
    _user_id.short_description = 'USER_ID'
    
    def _identificador(self, obj): return obj.identificador
    _identificador.short_description = 'IDENTIFICADOR'
    
    def _time(self, obj): return obj.time
    _time.short_description = 'TIME'

    # Lista de exibição com os nomes em MAIÚSCULO
    list_display = (
        '_id', 
        '_created_at', 
        '_descricao', 
        '_categoria', 
        '_valor', 
        '_tipo', 
        '_data', 
        '_esta_pago', 
        '_user_id', 
        '_identificador', 
        '_time'
    )
    
    list_filter = ("tipo", "categoria", "esta_pago", "data")
    search_fields = ("user__username", "identificador", "descricao", "categoria")
    readonly_fields = ("created_at", "time", "identificador")
    
    ordering = ("-created_at",)
