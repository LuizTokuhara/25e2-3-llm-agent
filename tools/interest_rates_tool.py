import requests
from langchain.tools import tool

class InterestRatesTool:
  def __init__(self):
    self.name = "get_rates"
    self.description = """
    Ferramenta para consultar taxa de juros
    """
  
  @tool
  def get_rates(query: str) -> str:
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
    return self.get_rates