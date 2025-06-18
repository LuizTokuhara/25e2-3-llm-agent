import os
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from tools.cripto_price_tool import CryptoPriceTool
from tools.interest_rates_tool import InterestRatesTool
from tools.cripto_history_tool import CryptoHistoryTool
from tools.cripto_exchanges_tool import CryptoExchangesTool
from memory.memory import Memory
from prompt.prompt import AgentPrompt
from datetime import date

class Agent:
  def __init__(self):
    """Inicializa o agente com ferramentas"""
    self.llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18",
                          openai_api_key=os.getenv("OPENAI_API_KEY"),
                          temperature=0.7)
    
    self.tools = [InterestRatesTool().get_tool(),
                  CryptoPriceTool().get_tool(),
                  CryptoHistoryTool().get_tool(),
                  CryptoExchangesTool().get_tool()]
    
    self.prompt = AgentPrompt().get_prompt()
    self.memory = Memory()

    self.executor = AgentExecutor(agent=create_openai_tools_agent(self.llm, self.tools, self.prompt),
                                  tools=self.tools,
                                  verbose=True)
    
    self.agent_with_history = RunnableWithMessageHistory(self.executor,
                                                         self.memory.get_history,
                                                         input_messages_key="input",
                                                         history_messages_key="chat_history")
    
  def chat(self, message: str, session_id: str) -> str:
    """Processa a mensagem do usuário e retorna a resposta do agente"""
    response = self.agent_with_history.invoke({"input": message, "today": str(date.today())},
                                              config={"configurable": {"session_id": session_id}})
    return response["output"]
