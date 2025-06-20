from langchain_core.prompts import (
  SystemMessagePromptTemplate, 
  ChatPromptTemplate, 
  HumanMessagePromptTemplate, 
  MessagesPlaceholder)

class AgentPrompt:
  def get_prompt(self):
    """Retorna o template de prompt para o agente."""

    system_message = """
    Você é um Assistente de Investimentos em Criptoativos que ajuda usuários com dicas de investimento.
    Seu papel é ajudar usuários a obter informações financeiras sobre criptoativos.

    Data de hoje: {today}

    ### Ferramentas disponíveis:
    {tools}

    ### Diretrizes:
    - Responda somente assuntos relacionados a finanças e investimentos.
    - Antes de responder, verifique se a pergunta não possui linguagem ofensiva ou imprópria.
    - Se a pergunta não for sobre finanças, informe que não pode ajudar com isso.

    Sempre responda de forma clara e resumida.
    Se não souber a resposta, seja honesto e educado.
    """

    return ChatPromptTemplate.from_messages(
      [
        SystemMessagePromptTemplate.from_template(system_message),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
      ]
    )
