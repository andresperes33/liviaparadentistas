import json
import logging
from django.utils import timezone
from users.models import User
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from .memory import ConversationMemory
from .router_prompt import ROUTER_AGENT_PROMPT
from .registrar_prompt import REGISTRAR_AGENT_PROMPT
from .deletar_prompt import DELETAR_AGENT_PROMPT
from .generico_prompt import GENERICO_AGENT_PROMPT
from .relatorios_prompt import RELATORIOS_AGENT_PROMPT
from .alterar_prompt import ALTERAR_AGENT_PROMPT
from .alterar_categoria_prompt import ALTERAR_CATEGORIA_AGENT_PROMPT
from .alterar_descricao_prompt import ALTERAR_DESCRICAO_AGENT_PROMPT
from .alterar_status_categoria_prompt import ALTERAR_STATUS_CATEGORIA_AGENT_PROMPT
from .alterar_valor_prompt import ALTERAR_VALOR_AGENT_PROMPT
from .consultas_prompt import CONSULTAS_AGENT_PROMPT
from .router_schema import LIVIA_TOOLS
from .tools_executor import TransactionToolsExecutor

logger = logging.getLogger("django")
# Autoreload trigger

class LiviaRouterBot:
    
    @staticmethod
    def _build_system_prompt() -> str:
        now_str = timezone.now().strftime("%d/%m/%Y %H:%M:%S")
        prompt = ROUTER_AGENT_PROMPT + "\n\n" + REGISTRAR_AGENT_PROMPT + "\n\n" + DELETAR_AGENT_PROMPT + "\n\n" + GENERICO_AGENT_PROMPT + "\n\n" + RELATORIOS_AGENT_PROMPT + "\n\n" + ALTERAR_AGENT_PROMPT + "\n\n" + ALTERAR_CATEGORIA_AGENT_PROMPT + "\n\n" + ALTERAR_DESCRICAO_AGENT_PROMPT + "\n\n" + ALTERAR_STATUS_CATEGORIA_AGENT_PROMPT + "\n\n" + ALTERAR_VALOR_AGENT_PROMPT + "\n\n" + CONSULTAS_AGENT_PROMPT
        prompt += f"\n\n[SISTEMA] DATA/HORA ATUAL DO EXECUTOR: {now_str}\n"
        return prompt

    @staticmethod
    def process_message(user: User, user_message: str, transaction) -> str:
        phone = user.phone
        ConversationMemory.add_message(phone, "user", user_message)
        history = ConversationMemory.get_history(phone)
        
        system_prompt = LiviaRouterBot._build_system_prompt()
        langchain_messages = [SystemMessage(content=system_prompt)]
        
        for msg in history:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                # Pulando mensagens de tool call antigas pra simplificar buffer
                if "tool_calls" in msg:
                    continue
                langchain_messages.append(AIMessage(content=msg["content"]))

        # Acopla a rede de Tools nativo na LangChain (bind_tools abstrai o "tool_choice")
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, max_tokens=800).bind_tools(LIVIA_TOOLS)
        
        max_loops = 3
        current_loop = 0
        
        while current_loop < max_loops:
            current_loop += 1
            try:
                response = llm.invoke(langchain_messages)
            except Exception as e:
                logger.error(f"[RouterBot] LangChain API falhou: {e}")
                return "Desculpe, meu sistema de registro está indisponível."

            langchain_messages.append(response)
            
            # 1) IA decidiu usar Tools
            if response.tool_calls:
                final_direct_response = None
                
                for tool_call in response.tool_calls:
                    executor_result = TransactionToolsExecutor.execute(
                        tool_name=tool_call["name"],
                        arguments=json.dumps(tool_call["args"]),
                        user=user,
                        transaction=transaction
                    )
                    
                    if executor_result["should_respond_directly"]:
                        final_direct_response = executor_result["content"]
                        
                    langchain_messages.append(
                        ToolMessage(
                            tool_call_id=tool_call["id"],
                            name=tool_call["name"],
                            content=executor_result["content"]
                        )
                    )
                
                # Se as execuções já produziram a interface visual de saída
                if final_direct_response:
                    ConversationMemory.add_message(phone, "assistant", final_direct_response)
                    return final_direct_response
                    
                continue

            # 2) Sem uso de ferramentas (resposta direta de Generico/Chat)
            else:
                ai_reply = response.content.strip()
                ConversationMemory.add_message(phone, "assistant", ai_reply)
                return ai_reply
                
        fallback = "Tive um problema ao conectar com minhas ferramentas internas."
        ConversationMemory.add_message(phone, "assistant", fallback)
        return fallback
