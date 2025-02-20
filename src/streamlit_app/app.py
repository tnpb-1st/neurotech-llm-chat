import streamlit as st
import pandas as pd
from src.llms.agents.query_validator import QueryValidator
from src.llms.agents.sql_executor import SQLExecutor
from src.llms.agents.insight_generator import InsightsGenerator
from config.constants import TABLE_INFO, NEUROCHAT_IMG


class DataChatApp:
    def __init__(self):
        # Cria um DataFrame com as informações do esquema da tabela
        self.schema_df = pd.DataFrame(TABLE_INFO)
        # Inicializa os agentes
        self.query_validator_agent = QueryValidator()
        self.sql_executor_agent = SQLExecutor()
        self.insights_generator_agent = InsightsGenerator()

    def run(self):
        st.title("Chatbot de Análise de Dados (SQL)")

        # Botão para reiniciar o chat
        if st.button("Novo Chat", type="primary"):
            st.rerun()

        initial_message = (
            "Olá. Eu sou o Neurochat, estou aqui para ser seu assistente de análise de dados. Confira abaixo as "
            "informações do Banco de Dados. Você pode me fazer perguntas ou consultas sobre esses dados e eu irei te "
            "ajudar a responder. Vamos lá!"
        )

        with st.chat_message("assistant", avatar=NEUROCHAT_IMG):
            st.write(initial_message)
            st.dataframe(self.schema_df, hide_index=True)

        # Captura o input do usuário
        if prompt := st.chat_input("Escreva seu comando para o neurochat: "):
            with st.chat_message("user"):
                st.write(prompt)

            # Validação do input
            st.write("Validando input...🔍")
            validate_status, reason = self.query_validator_agent.validate_query(prompt)
            is_valid = validate_status == "valid"

            with st.chat_message("assistant", avatar=NEUROCHAT_IMG):
                if is_valid:
                    st.write("Input válido✅")
                    st.write("Processando Query SQL...🔄")
                    query_result = self.sql_executor_agent.run(prompt)
                    if "error" in query_result:
                        st.warning(
                            f"Erro ao processar a query SQL: {query_result['error']} "
                            "Por favor, tente novamente!"
                        )
                    else:
                        st.write("Query SQL processada com sucesso✅")
                        st.write("Exibindo os resultados...📊")
                        st.code(query_result["sql_query"], language="sql")
                        st.dataframe(query_result["data"], hide_index=True)
                        if "data" in query_result and len(query_result["data"]) > 0:
                            # Adiciona o input original no dicionário para gerar os insights
                            insight_dir = query_result
                            insight_dir["input"] = prompt
                            st.write("Gerando insights...📊")
                            insights = self.insights_generator_agent.generate_insights(
                                insight_dir
                            )
                            st.write(insights)
                        st.write("Fim da Análise!🎉")
                else:
                    st.warning(
                        f"Requisição inválida‼️\nSeu input foi considerado inválido por: {reason} "
                        "Por favor, tente novamente!"
                    )


if __name__ == "__main__":
    app = DataChatApp()
    app.run()
