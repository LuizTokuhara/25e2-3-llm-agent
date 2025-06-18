import requests
from langchain.tools import StructuredTool

class CryptoPriceTool:
  def __init__(self):
    self.name = "get_crypto_price"
    self.description = """"
    Ferramenta para consultar o valor atual de criptomoedas.
    Utilize essa ferramenta sempre que o usuário solicitar o preço atual de uma ou mais criptomoedas, como:
    - "Qual o valor do Bitcoin hoje?"
    - "Quanto está o Ethereum agora?"
    """

  def get_crypto_price(self, query: str) -> str:
    """Consulta o valor atual de uma criptomoeda."""

    api_url = "https://api.coingecko.com/api/v3/simple/price"
    coins = [coin.strip().lower() for coin in query.split(",")]
    params = {"ids": ",".join(coins), "vs_currencies": "brl"}

    try:
      response = requests.get(api_url, params=params)
      data = response.json()
      result = []
      for coin in coins:
        price = data.get(coin, {}).get("brl")
        if price:
          result.append(f"{coin.capitalize()}: R$ {price:.2f}")
        else:
          result.append(f"{coin.capitalize()}: Valor não encontrado")
      return "\n".join(result)
    except Exception as e:
      return f"Erro ao consultar valores: {str(e)}"
  
  def get_tool(self):
    """Retorna a instância da ferramenta."""
    return StructuredTool.from_function(func=self.get_crypto_price,
                                        name=self.name,
                                        description=self.description)