import streamlit as st
import pandas as pd
from src.llms.agents.query_validator import QueryValidator
from src.llms.agents.sql_executor import SQLExecutor

# Certifique-se de que este caminho esteja correto
from config.constants import (
    TABLE_INFO,
)  # Certifique-se de que este caminho esteja correto

from langchain_openai import ChatOpenAI

# Cria um DataFrame com as informações da tabela
SCHEMA_DF = pd.DataFrame(TABLE_INFO)

st.title("Chatbot de Análise de Dados (SQL)")
col1 = st.columns([0.2])[0]

# with col1:
if st.button("Novo Chat", type="primary"):
    st.rerun()


initial_message = (
    "Olá . Eu sou o Neurochat, estou aqui para ser seu assistente de análise de dados. Confira abaixo as "
    "informações do Banco de Dados. Você pode me fazer perguntas ou consultas sobre esses dados que eu ir"
    "ei te ajudar a responder. Vamos lá!"
)

with st.chat_message("assistant"):
    st.write(initial_message)
    st.dataframe(SCHEMA_DF, hide_index=True)

if prompt := st.chat_input("Escreva seu comando para o neurochat: "):
    with st.chat_message("user"):
        st.write(prompt)

    # VALIDATE INPUT
    query_validator = QueryValidator()
    st.write("Validando input...🔍")
    validate_status, reason = query_validator.validate_query(prompt)
    is_valid = validate_status == "valid"
    with st.chat_message("assistant"):
        if is_valid:
            st.write("Input valido✅")
            st.write("Processando Query SQL...🔄")
            # final_response = {"sql_query": sql_query, "data": query_result["data"]}
            # final_response = {"error": ...}
            query_result = SQLExecutor().run(prompt)
            if "error" in query_result:
                st.warning(
                    f"Erro ao processar a query SQL: {query_result['error']}"
                    "Por favor, tente novamente!"
                )
            else:
                st.write("Query SQL processada com sucesso✅")
                st.write("Exibindo os resultados...📊")
                st.code(query_result["sql_query"], language="sql")
                st.dataframe(query_result["data"], hide_index=True)
        else:
            st.warning(
                f"Requisição inválida‼️\nSeu input foi considerado ivalid por: {reason}"
                "Por favor, tente novamente!"
            )
