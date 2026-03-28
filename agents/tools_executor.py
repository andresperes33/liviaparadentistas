import logging
import json
import datetime
import re
from django.db.models import Sum
from users.models import User
from transactions.models import Transaction

logger = logging.getLogger("django")

class TransactionToolsExecutor:
    """Implementa as lógicas de negócio no banco ativadas pelos Tool Calls da OpenAI."""

    @staticmethod
    def execute(tool_name: str, arguments: str, user: User, transaction=None) -> dict:
        """
        Interpreta o JSON do Tool e aciona o método Python correto.
        """
        try:
            kwargs = json.loads(arguments)
        except json.JSONDecodeError:
            kwargs = {}
            
        logger.info(f"[ToolExecutor] Acionando {tool_name} para {user.username} | Args: {kwargs}")

        if tool_name == "think":
            return {"should_respond_directly": False, "content": "Análise concluída. Executando próxima ação..."}
            
        elif tool_name == "Generico":
            msg = kwargs.get("mensagem", "")
            return {"should_respond_directly": True, "content": msg}
            
        elif tool_name == "Registrar":
            return TransactionToolsExecutor._tool_registrar(user, transaction, **kwargs)
            
        elif tool_name == "Consultas":
            return TransactionToolsExecutor._tool_consultas(user, **kwargs)
            
        elif tool_name == "Alterar_Status_Categoria":
            return TransactionToolsExecutor._tool_alterar_status_categoria(user, **kwargs)
            
        elif tool_name == "Deletar":
            return TransactionToolsExecutor._tool_deletar(user, **kwargs)
            
        elif tool_name in ["Alterar", "Alterar_Categoria", "Alterar_Descricao", "Alterar_Valor"]:
            return TransactionToolsExecutor._tool_alterar_individual(user, tool_name, **kwargs)
            
        elif tool_name == "Relatorios":
            return TransactionToolsExecutor._tool_relatorios(user, **kwargs)
            
        else:
            return {"should_respond_directly": False, "content": f"Ferramenta desconhecida: {tool_name}"}

    @staticmethod
    def _tool_registrar(user: User, transaction, tipo: str, valor: float, descricao: str, categoria: str, data: str, status: str):
        if not transaction:
            transaction = Transaction.objects.create(user=user)
            
        transaction.tipo = tipo
        # Garantir valor positivo para o banco, a lógica de sinal pode ser tratada na exibição ou conforme o tipo
        # No modelo original, despesas parecem ser salvas com sinal negativo conforme um comentário, 
        # mas o prompt diz "Valores de despesa devem ser negativos".
        transaction.valor = float(valor)
        transaction.descricao = descricao
        transaction.categoria = categoria.lower() if categoria else "padrão"
        transaction.status_pagamento = status
        
        if data:
            match = re.search(r"(\d{2})[-/](\d{2})[-/](\d{4})", data)
            if match:
                d, m, y = match.groups()
                transaction.data_transacao = datetime.date(int(y), int(m), int(d))
            else:
                transaction.data_transacao = datetime.date.today()
        else:
            transaction.data_transacao = datetime.date.today()
            
        transaction.is_financial = True
        transaction.save()
        
        markdown = f"✅ *{tipo} Registrada com sucesso!*\n\n"
        markdown += f"🆔 ID: {transaction.id}\n"
        markdown += f"💰 Valor: R$ {abs(float(valor)):.2f}\n"
        markdown += f"🏷️ Tipo: {'📈' if tipo == 'Receita' else '📉'} {tipo}\n"
        markdown += f"📄 Descrição: {descricao}\n"
        markdown += f"🏷️ Categoria: {categoria}\n"
        markdown += f"📅 Data: {transaction.data_transacao.strftime('%d-%m-%Y')}\n"
        markdown += f"📌 Status: {status}\n\n"
        markdown += f"❌ Para excluir ou editar, envie: {transaction.id}"
        return {"should_respond_directly": True, "content": markdown}

    @staticmethod
    def _tool_consultas(user: User, **kwargs):
        tipo = kwargs.get("tipo")
        categoria = kwargs.get("categoria", "").lower()
        status = kwargs.get("status")

        qs = Transaction.objects.filter(user=user, is_financial=True)
        if tipo:
            qs = qs.filter(tipo=tipo)
        if categoria:
            qs = qs.filter(categoria=categoria)
        if status and status != "Todos":
            qs = qs.filter(status_pagamento=status)

        return TransactionToolsExecutor._build_report_markdown(qs, f"Consulta: {categoria or 'Geral'}")

    @staticmethod
    def _tool_alterar_status_categoria(user: User, categoria: str):
        categoria_norm = categoria.lower()
        qs = Transaction.objects.filter(user=user, categoria=categoria_norm, status_pagamento="A receber")
        count = qs.count()
        total = qs.aggregate(Sum('valor'))['valor__sum'] or 0
        
        qs.update(status_pagamento="Pago")
        
        markdown = f"✅ *Liquidação Concluída - {categoria.title()}*\n\n"
        markdown += f"Foram atualizados *{count} registro(s)* da categoria *{categoria.title()}*.\n"
        markdown += "Todas as transações foram marcadas como *Pagas*.\n\n"
        markdown += f"💰 *Total liquidado:* R$ {abs(float(total)):.2f}\n\n"
        markdown += "🎉 Operação realizada com sucesso!"
        
        return {"should_respond_directly": True, "content": markdown}

    @staticmethod
    def _tool_deletar(user: User, codigo: str):
        try:
            trans = Transaction.objects.get(id=codigo.upper(), user=user)
            desc = trans.descricao
            valor = trans.valor
            trans.delete()
            
            markdown = f"✅ Foi excluída a transação {codigo.upper()}\n"
            markdown += f"🔖 *Descrição:* {desc}\n"
            markdown += f"💸 *Valor:* R$ {abs(float(valor)):.2f}"
            return {"should_respond_directly": True, "content": markdown}
        except Transaction.DoesNotExist:
            return {"should_respond_directly": True, "content": f"❌ Transação {codigo.upper()} não encontrada."}

    @staticmethod
    def _tool_alterar_individual(user: User, tool_name: str, **kwargs):
        codigo = kwargs.get("codigo") or kwargs.get("identificador")
        if not codigo:
            return {"should_respond_directly": True, "content": "❌ Código da transação não fornecido."}
            
        try:
            trans = Transaction.objects.get(id=codigo.upper(), user=user)
            
            if tool_name == "Alterar": # Geralmente status para Pago
                trans.status_pagamento = "Pago"
            elif tool_name == "Alterar_Categoria":
                trans.categoria = kwargs.get("nova_categoria", "").lower()
            elif tool_name == "Alterar_Descricao":
                trans.descricao = kwargs.get("nova_descricao")
            elif tool_name == "Alterar_Valor":
                # Limpeza de valor já deve ter sido vinda da IA, mas garantimos
                novo_valor = kwargs.get("novo_valor")
                if isinstance(novo_valor, str):
                    novo_valor = re.sub(r"[^\d,.-]", "", novo_valor).replace(",", ".")
                trans.valor = float(novo_valor)
            
            trans.save()
            
            markdown = f"✅ Foi alterada a transação {trans.id}\n\n"
            markdown += f"🔖 *Descrição:* {trans.descricao}\n"
            markdown += f"🏷️ *Categoria:* {trans.categoria.title()}\n"
            markdown += f"📌 *Status:* {trans.status_pagamento}\n"
            markdown += f"💸 *Valor:* R$ {abs(float(trans.valor)):.2f}"
            return {"should_respond_directly": True, "content": markdown}
            
        except Transaction.DoesNotExist:
            return {"should_respond_directly": True, "content": f"❌ Transação {codigo.upper()} não encontrada."}
        except Exception as e:
            return {"should_respond_directly": True, "content": f"❌ Erro ao alterar: {str(e)}"}

    @staticmethod
    def _tool_relatorios(user: User, **kwargs):
        mes = kwargs.get("mes")
        ano = kwargs.get("ano")
        
        qs = Transaction.objects.filter(user=user, is_financial=True)
        
        if mes:
            qs = qs.filter(data_transacao__month=int(mes))
        if ano:
            qs = qs.filter(data_transacao__year=int(ano))
        else:
            # Se não informou ano, usa o atual
            qs = qs.filter(data_transacao__year=datetime.date.today().year)
            
        title = f"Relatório Mensal - {mes}/{ano or datetime.date.today().year}"
        return TransactionToolsExecutor._build_report_markdown(qs, title)

    @staticmethod
    def _build_report_markdown(qs, title: str):
        # Receitas Pagas
        rec_pagas_qs = qs.filter(tipo="Receita", status_pagamento="Pago")
        rec_pagas_total = rec_pagas_qs.aggregate(Sum('valor'))['valor__sum'] or 0
        
        # Despesas Pagas
        desp_pagas_qs = qs.filter(tipo="Despesa", status_pagamento="Pago")
        desp_pagas_total = desp_pagas_qs.aggregate(Sum('valor'))['valor__sum'] or 0
        
        # Receitas A Receber
        rec_pendentes_qs = qs.filter(tipo="Receita", status_pagamento="A receber")
        rec_pendentes_total = rec_pendentes_qs.aggregate(Sum('valor'))['valor__sum'] or 0
        
        # Cálculos de Saldo
        saldo_realizado = float(rec_pagas_total) + float(desp_pagas_total)
        saldo_projetado = saldo_realizado + float(rec_pendentes_total)
        
        def get_status_emoji(val):
            if val > 0: return "🟢 POSITIVO"
            if val < 0: return "🔴 NEGATIVO"
            return "⚖️ EQUILIBRADO"

        markdown = f"📊 *{title.upper()}*\n"
        markdown += "━━━━━━━━━━━━━━━━━━━━\n\n"
        
        markdown += "💰 *RESUMO FINANCEIRO*\n\n"
        markdown += f"🟢 Receitas Pagas: R$ {abs(float(rec_pagas_total)):.2f}\n"
        markdown += f"🔴 Despesas Pagas: R$ {abs(float(desp_pagas_total)):.2f}\n"
        markdown += "➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        markdown += f"💵 *SALDO REALIZADO:* R$ {saldo_realizado:.2f}\n"
        markdown += f"📊 SITUAÇÃO: {get_status_emoji(saldo_realizado)}\n\n"
        
        markdown += "━━━━━━━━━━━━━━━━━━━━\n\n"
        markdown += "⏳ *VALORES A RECEBER*\n\n"
        markdown += f"🟡 Receitas A Receber: R$ {abs(float(rec_pendentes_total)):.2f}\n"
        markdown += "➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        markdown += f"💰 *SALDO PROJETADO:* R$ {saldo_projetado:.2f}\n"
        markdown += f"📊 SITUAÇÃO: {get_status_emoji(saldo_projetado)}\n\n"
        
        markdown += "━━━━━━━━━━━━━━━━━━━━\n\n"
        markdown += "📋 *DETALHAMENTO POR CATEGORIA:*\n\n"
        
        # Agrupar por categoria
        categorias = qs.values_list('categoria', flat=True).distinct()
        for cat in categorias:
            cat_qs = qs.filter(categoria=cat)
            cat_rec_p = cat_qs.filter(tipo="Receita", status_pagamento="Pago").aggregate(Sum('valor'))['valor__sum'] or 0
            cat_desp_p = cat_qs.filter(tipo="Despesa", status_pagamento="Pago").aggregate(Sum('valor'))['valor__sum'] or 0
            cat_rec_a = cat_qs.filter(tipo="Receita", status_pagamento="A receber").aggregate(Sum('valor'))['valor__sum'] or 0
            
            cat_realizado = float(cat_rec_p) + float(cat_desp_p)
            cat_projetado = cat_realizado + float(cat_rec_a)
            
            markdown += f"🏷️ *{cat.title()}*\n"
            markdown += f"   💵 Realizado: R$ {cat_realizado:.2f} {'🟢' if cat_realizado >= 0 else '🔴'}\n"
            markdown += f"   💰 Projetado: R$ {cat_projetado:.2f} {'🟢' if cat_projetado >= 0 else '🔴'}\n\n"

        markdown += "━━━━━━━━━━━━━━━━━━━━\n\n"
        markdown += "📋 *TRANSAÇÕES:*\n\n"
        
        for trans in qs.order_by('-data_transacao')[:15]: # Limite de 15 para não estourar WhatsApp
            emoji = "🟢" if trans.tipo == "Receita" and trans.status_pagamento == "Pago" else \
                    "🔴" if trans.tipo == "Despesa" else "🟡"
            status_txt = "Pago" if trans.status_pagamento == "Pago" else "A receber"
            
            markdown += f"{emoji} ID: {trans.id} | R$ {abs(float(trans.valor)):.2f} | {trans.descricao[:20]} | {trans.data_transacao.strftime('%d/%m')} | {status_txt}\n"

        if qs.count() > 15:
            markdown += "\n*... e mais registros disponíveis no sistema.*"

        return {"should_respond_directly": True, "content": markdown}
