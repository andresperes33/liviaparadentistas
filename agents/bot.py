from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from .memory import ConversationMemory
import logging
from .prompts import SALES_AGENT_PROMPT, RENEWAL_AGENT_PROMPT

logger = logging.getLogger("django")

class LiviaAgentService:
    @staticmethod
    def get_agent_response(telefone: str, user_message: str, agent_type: str = "sales") -> str:
        """
        Consulta o histórico no Redis e chama a IA na LangChain com o prompt adequado.
        """
        ConversationMemory.add_message(telefone, "user", user_message)
        history = ConversationMemory.get_history(telefone)
        
        system_prompt = SALES_AGENT_PROMPT if agent_type == "sales" else RENEWAL_AGENT_PROMPT
        
        # Converte as mensagens do formato interno pra LangChain
        langchain_messages = [SystemMessage(content=system_prompt)]
        for msg in history:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
        
        try:
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, max_tokens=600)
            response = llm.invoke(langchain_messages)
            
            ai_reply = response.content.strip()
            ConversationMemory.add_message(telefone, "assistant", ai_reply)
            return ai_reply
            
        except Exception as e:
            logger.error(f"[BotService] LangChain API falhou: {e}")
            fallback = "Desculpe, estou em manutenção e não pude processar sua mensagem."
            ConversationMemory.add_message(telefone, "assistant", fallback)
            return fallback
