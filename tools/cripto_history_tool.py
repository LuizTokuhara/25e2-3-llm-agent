import requests
from langchain.tools import StructuredTool
from datetime import datetime

class CryptoHistoryTool:
  def __init__(self):
    self.name = "get_crypto_history"
    self.description = """
    Ferramenta para consultar o histórico de preços de uma criptomoeda entre duas datas.

    Esta ferramenta deve ser usada sempre que o usuário solicitar informações sobre o preço de uma criptomoeda ao longo do tempo, como:
    - "Qual foi o valor do Bitcoin nos últimos 15 dias?"
    - "Me mostre os preços da Solana entre 1 e 10 de maio."

    ### Parâmetros:
    - crypto (obrigatório): nome da criptomoeda.
    - start_date (obrigatório): data de início no formato YYYY-MM-DD
    - end_date (obrigatório): data de fim no formato YYYY-MM-DD

    A resposta trará o valor de fechamento (em reais) de cada dia dentro do intervalo especificado.
    """

  def resolve_symbol(self, cripto: str) -> str:
    """Consulta o símbolo da criptomoeda."""
    query = cripto.lower().strip()
    url = f"https://api.coingecko.com/api/v3/search?query={query}"

    try:
      response = requests.get(url)
      data = response.json()
      coins = data.get("coins", [])

      if not coins:
        return None
      
      symbol = coins[0].get("symbol", "").upper()
      return f"{symbol}-BRL"
    except Exception as e:
      return None
    
  def get_history(self, crypto: str, start_date: str, end_date: str) -> str:
    try:
      start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
      end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

      url = f"https://api.coingecko.com/api/v3/coins/{crypto.lower()}/market_chart/range"
      params = {
        "vs_currency": "brl",
        "from": start_ts,
        "to": end_ts
      }

      res = requests.get(url, params=params)
      if res.status_code != 200:
        return f"Erro ao buscar dados: {res.status_code} - {res.text}"

      prices = res.json().get("prices", [])
      if not prices:
        return f"Nenhum dado de preço encontrado para {crypto}."

      response = f"Histórico de preços de {crypto.capitalize()} entre {start_date} e {end_date}:\n"
      seen_dates = set()

      for price in prices:
        dt = datetime.fromtimestamp(price[0] / 1000)
        date_str = dt.strftime("%Y-%m-%d")
        if date_str not in seen_dates:
          seen_dates.add(date_str)
          response += f"{dt.strftime('%d/%m')}: R$ {price[1]:.2f}\n"

      return response.strip()

    except Exception as e:
      return f"Erro ao processar os dados: {str(e)}"
  
  def get_tool(self):
    """Retorna a instância da ferramenta."""
    return StructuredTool.from_function(func=self.get_history,
                                        name=self.name,
                                        description=self.description)