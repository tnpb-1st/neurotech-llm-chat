import streamlit as st
import pandas as pd
from src.llms.agents.query_validator import QueryValidator
from src.llms.agents.sql_executor import SQLExecutor
from src.llms.agents.insight_generator import InsightsGenerator
from langchain_openai import ChatOpenAI
from config.constants import TABLE_INFO


# Cria um DataFrame com as informações da tabela
SCHEMA_DF = pd.DataFrame(TABLE_INFO)
QUERY_VALIDATOR_AGENT = QueryValidator()
SQL_EXECUTOR_AGENT = SQLExecutor()
INSIGHTS_GENERATOR_AGENT = InsightsGenerator()


# Streamlit
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
    st.write("Validando input...🔍")
    validate_status, reason = QUERY_VALIDATOR_AGENT.validate_query(prompt)
    is_valid = validate_status == "valid"
    with st.chat_message("assistant"):
        if is_valid:
            st.write("Input valido✅")
            st.write("Processando Query SQL...🔄")
            # final_response = {"sql_query": sql_query, "data": query_result["data"]}
            # final_response = {"error": ...}
            query_result = SQL_EXECUTOR_AGENT.run(prompt)
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
                if "data" in query_result and len(query_result["data"]) > 0:
                    insight_dir = query_result
                    insight_dir["input"] = prompt
                    st.write("Gerando insights...📊")
                    insights = INSIGHTS_GENERATOR_AGENT.generate_insights(insight_dir)
                    st.write(insights)

        else:
            st.warning(
                f"Requisição inválida‼️\nSeu input foi considerado ivalid por: {reason}"
                "Por favor, tente novamente!"
            )
