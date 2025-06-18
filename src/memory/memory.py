from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory

class Memory:
  def __init__(self):
    """Inicializa a memória com histórico de mensagens"""
    self.history = {}
  
  def get_history(self, session_id: str) -> BaseChatMessageHistory:
    """Retorna o histórico de mensagens para uma sessão específica"""
    if session_id not in self.history:
      self.history[session_id] = InMemoryChatMessageHistory()
    return self.history[session_id]