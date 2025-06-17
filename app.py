import uuid
import time
import streamlit as st
from dotenv import load_dotenv
from agents.agent import Agent

load_dotenv()

st.set_page_config(page_title="Assistente de Investimentos em Criptoativos",
                   page_icon=":money_with_wings:")
st.header("Assistente de Investimentos em Criptoativos")
with st.expander("⚠️  **Aviso Importante:**"):
  st.write(
    """
    Este assistente de investimentos é um **estudo de caso e uma demonstração tecnológica**.
    As informações e sugestões fornecidas são geradas por IA e **não devem ser consideradas como aconselhamento
    financeiro ou recomendações de investimento**.
    """
  )

if "session_id" not in st.session_state:
  st.session_state.session_id = uuid.uuid4()
if "messages" not in st.session_state:
  st.session_state.messages = []
if "agent" not in st.session_state:
  st.session_state.agent = Agent()

agent = st.session_state.agent

def simulate_stream_data(data: str):
  """Simula o streaming de dados para o chat"""
  for word in data.split(" "):
    yield word + " "
    time.sleep(0.02)

for msg in st.session_state.messages:
  with st.chat_message(msg["role"]):
    st.markdown(msg["content"])

if prompt_user := st.chat_input("Digite sua mensagem..."):
  st.session_state.messages.append({"role": "user", "content": prompt_user})
  with st.chat_message("user"):
    st.markdown(prompt_user)

  with st.chat_message("assistant"):
    with st.spinner("Pensando..."):
      answer = agent.chat(prompt_user, st.session_state.session_id)
      st.write_stream(simulate_stream_data(answer))

  st.session_state.messages.append({"role": "assistant", "content": answer})
