import streamlit as st
import pandas as pd
from src.streamlit_app.templates import TABLE_INFO
from src.config.constants import OPENAI_MODEL


SCHEMA_DF = pd.DataFrame(TABLE_INFO)

st.title("Chatbot de Análise de Dados (SQL) e Visualização")

with st.chat_message("assistant"):
    st.write(
        "Olá 👋. Eu sou o Neurochat, estou aqui para ser seu assistente de análise de dados. Confira abaixo as informações do Banco de Dados:"
    )
    # Display table in Streamlit
    st.table(SCHEMA_DF)
