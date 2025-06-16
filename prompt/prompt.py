from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from datetime import date

class AgentPrompt:
  def get_prompt(self):
    """Retorna o template de prompt para o agente."""
    today = date.today()

    system_message = """
    Você é um assistente financeiro que ajuda usuários com dicas de investimento.
    Seu papel é ajudar usuários a obter informações financeiras sobre criptoativos.

    Data de hoje: {today}

    ### Ferramentas disponíveis:
    - **get_crypto_price**: Consulta o valor atual de criptomoedas.
    - **get_rates**: Consulta a taxa de juros da Selic, CDI e IPCA atuais.

    Sempre responda de forma clara e resumida.
    Se não souber a resposta, seja honesto e educado.
    """.format(today=today)

    return ChatPromptTemplate.from_messages(
      [
        ("system", system_message),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
      ]
    )