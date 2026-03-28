LIVIA_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "think",
            "description": "Utilizada para criar um raciocínio interno antes de registrar ou tomar decisões. Nunca exposto ao usuário.",
            "parameters": {
                "type": "object",
                "properties": {
                    "analise": {"type": "string", "description": "Resumo estruturado dos dados inferidos (tipo, status, etc)."}
                },
                "required": ["analise"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Registrar",
            "description": "Registra uma nova transação financeira (receita ou despesa) no sistema contábil.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tipo": {"type": "string", "enum": ["Receita", "Despesa"], "description": "O tipo da transação."},
                    "valor": {"type": "number", "description": "O valor da transação em numérico com casas decimais (ex: 150.50). Valores de despesa devem ser negativos."},
                    "descricao": {"type": "string", "description": "Descrição detalhada do registro."},
                    "categoria": {"type": "string", "description": "Categoria associada (normalizada e sem acentos)."},
                    "data": {"type": "string", "description": "Data da transação (formato dd-mm-yyyy). Se não mencionada usar data de hoje."},
                    "status": {"type": "string", "enum": ["Pago", "A receber"], "description": "Status de pagamento. Despesas são sempre 'Pago'."}
                },
                "required": ["tipo", "valor", "descricao", "categoria", "data", "status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Consultas",
            "description": "Verifica pendências de recebimento agrupadas por categoria.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tipo": {"type": "string", "enum": ["Receita", "Despesa"], "description": "O tipo da consulta."},
                    "categoria": {"type": "string", "description": "Nome da categoria a ser consultada."},
                    "status": {"type": "string", "enum": ["Pago", "A receber", "Todos"], "description": "Status da consulta."}
                },
                "required": ["tipo", "categoria", "status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Alterar_Status_Categoria",
            "description": "Marca todas as transações 'A receber' de uma determinada categoria como 'Pago'. Utilizado para liquidar pendências de um cliente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "categoria": {"type": "string", "description": "A categoria/cliente a ser liquidado."}
                },
                "required": ["categoria"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Deletar",
            "description": "Exclui permanentemente uma transação pelo ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {"type": "string", "description": "O código exclusivo de 3 ou mais caracteres da transação."}
                },
                "required": ["codigo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Alterar",
            "description": "Altera o status de uma transação específica para 'Pago'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {"type": "string", "description": "O código da transação."}
                },
                "required": ["codigo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Alterar_Categoria",
            "description": "Altera a categoria de uma transação específica.",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {"type": "string", "description": "O código da transação."},
                    "nova_categoria": {"type": "string", "description": "O nome da nova categoria formatada."}
                },
                "required": ["codigo", "nova_categoria"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Alterar_Descricao",
            "description": "Altera a descrição textual de uma transação específica.",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {"type": "string", "description": "O código da transação."},
                    "nova_descricao": {"type": "string", "description": "A nova descrição completa."}
                },
                "required": ["codigo", "nova_descricao"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Alterar_Valor",
            "description": "Altera o valor numérico de uma transação específica.",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo": {"type": "string", "description": "O código da transação."},
                    "novo_valor": {"type": "number", "description": "O novo valor da transação (aceita decimais com ponto)."}
                },
                "required": ["codigo", "novo_valor"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Relatorios",
            "description": "Retorna o balanço descritivo do fluxo e relatórios consolidados.",
            "parameters": {
                "type": "object",
                "properties": {
                    "mes": {"type": "string", "description": "Mês (MM)."},
                    "ano": {"type": "string", "description": "Ano (YYYY)."}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Generico",
            "description": "Responde e interage diretamente com mensagens informais (olá, bom dia), dúvidas não relacionadas ou agradecimentos do usuário. NUNCA utilize como primeira ação se uma ação financeira foi disparada.",
            "parameters": {
                "type": "object",
                "properties": {
                    "mensagem": {"type": "string", "description": "Mensagem empática e direta que o Agente passará para o usuário final."}
                },
                "required": ["mensagem"]
            }
        }
    }
]
