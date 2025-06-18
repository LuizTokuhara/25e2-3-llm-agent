import requests
from langchain.tools import StructuredTool

class InterestRatesTool:
  def __init__(self):
    self.name = "get_rates"
    self.description = """
    Ferramenta para consultar taxa de juros atuais como Selic, CDI e IPCA.
    """
  
  def get_rates(self) -> str:
    """Consulta a taxa de juros da Selic, CDI e IPCA atuais."""

    api_url = "https://brasilapi.com.br/api/taxas/v1"
    
    try:
      response = requests.get(api_url)
      data = response.json()
      return data
    except Exception as e:
      return f"Erro ao consultar taxas: {str(e)}"
    
  def get_tool(self):
    """Retorna a instância da ferramenta."""
    return StructuredTool.from_function(func=self.get_rates,
                                        name=self.name,
                                        description=self.description)