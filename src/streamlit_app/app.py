import streamlit as st
import pandas as pd
# Certifique-se de que este caminho esteja correto
from src.config.constants import (
    OPENAI_MODEL,
    OPENAI_API_KEY,
    TABLE_INFO
)  # Certifique-se de que este caminho esteja correto

from langchain_openai import ChatOpenAI

# Cria um DataFrame com as informações da tabela
SCHEMA_DF = pd.DataFrame(TABLE_INFO)

st.title("Chatbot de Análise de Dados (SQL)")
col1 = st.columns([0.2])[0]

# with col1:
if st.button("Novo Chat", type="primary"):
    st.rerun()

# Inicializa o cliente do LangChain com o ChatOpenAI
chat = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key=OPENAI_API_KEY,
    streaming=True,
)

initial_message = (
    "Olá . Eu sou o Neurochat, estou aqui para ser seu assistente de análise de dados. Confira abaixo as "
    "informações do Banco de Dados. Você pode me fazer perguntas ou consultas sobre esses dados que eu ir"
    "ei te ajudar a responder. Vamos lá!"
)

with st.chat_message("assistant"):
    st.markdown(initial_message)
    st.dataframe(SCHEMA_DF, hide_index=True)

if prompt := st.chat_input("Escreva seu comando para o neurochat: "):
    with st.chat_message("user"):
        st.markdown(prompt)

    # VALIDATE INPUT
    is_valid = False
    with st.chat_message("assistant"):
        if is_valid:
            st.markdown("Input valido")
        else:
            st.warning("Input inválido. Por favor inicie um novo chat!")
