import requests
from bs4 import BeautifulSoup
from langchain.tools import StructuredTool

class CryptoExchangesTool:
  def __init__(self):
    self.name = "get_crypto_exchanges"
    self.description = """"
    Ferramenta para consultar as principais exchanges / corretoras de criptomoedas do Brasil.
    Utilize essa ferramenta sempre que o usuário solicitar informações sobre onde comprar ou vender criptomoedas
    no Brasil, como:
    - "Quais são as principais exchanges de criptomoedas no Brasil?""
    - "Onde posso comprar Bitcoin?"
    - "Quais corretoras oferecem negociação de criptomoedas?"
    
    Sempre retorne uma lista com os nomes das corretoras e avise o usuário que a lista foi obtida no site
    https://www.idinheiro.com.br/investimentos/corretoras/melhores-corretoras-criptomoedas/
    Avise o usuário que é importante pesquisar e comparar as taxas, segurança e variedade de criptomoedas de cada
    exchange antes de escolher onde investir.

    ### Exemplo de resposta:
    É importante pesquisar e comparar as taxas, segurança e variedade de criptomoedas de cada exchange antes de escolher onde investir.
    - Binance
    - Mercado Bitcoin
    - Bitso

    *Fonte: https://www.idinheiro.com.br/investimentos/corretoras/melhores-corretoras-criptomoedas/
    """

  def get_exchanges(self) -> str:
    """Consulta a lista de exchanges de criptomoedas no Brasil."""

    header = {
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    api_url = "https://www.idinheiro.com.br/investimentos/corretoras/melhores-corretoras-criptomoedas/"
    try:
      response = requests.get(api_url, headers=header)
      response.raise_for_status()
      html = response.content
      soup = BeautifulSoup(html, "html.parser")
      names = soup.select("table tbody tr td p")
      exchanges = [name.get_text() for name in names]

      if (not exchanges):
        return "Nenhuma corretora encontrada."
      
      return exchanges
    except Exception as e:
      return f"Erro ao consultar corretoras: {str(e)}"
    
  def get_tool(self):
    """Retorna a instância da ferramenta."""
    return StructuredTool.from_function(func=self.get_exchanges,
                                        name=self.name,
                                        description=self.description)
