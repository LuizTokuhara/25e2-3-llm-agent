import uuid
import streamlit as st
from dotenv import load_dotenv
from agents.agent import Agent

load_dotenv()

st.set_page_config(page_title="Assistente de Investimentos em Criptoativos",
                   page_icon=":money_with_wings:")
st.header("Assistente de Investimentos em Criptoativos")

if "session_id" not in st.session_state:
  st.session_state.session_id = uuid.uuid4()
if "messages" not in st.session_state:
  st.session_state.messages = []
if "agent" not in st.session_state:
  st.session_state.agent = Agent()

agent = st.session_state.agent

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
      st.markdown(answer)

  st.session_state.messages.append({"role": "assistant", "content": answer})
