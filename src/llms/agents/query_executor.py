from typing import Dict
import duckdb
import pandas as pd
from langchain_core.prompts.prompt import PromptTemplate
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from config.constants import (
    OPENAI_MODEL,
    OPENAI_API_KEY,
    TABLE_INFO,
)
from src.llms.prompts.prompts import SQL_GENERATOR_TEMPLATE
from src.llms.parsers.sql_output_parser import SQLQueryOutputParser
from src.data_access.connector import DBConnector


# --------------------------------------------------------------------------------
# Ferramentas (tools)
# --------------------------------------------------------------------------------


# noinspection SqlNoDataSourceInspection
@tool
def check_sql_syntax(sql: str) -> bool:
    """
    Valida a sintaxe SQL usando DuckDB com uma estrutura de tabela similar à tabela real V1.
    Args:
        sql: String da query SQL a ser validada
    Retorna:
        bool: True se a sintaxe for válida, False caso contrário
    """
    try:
        # Create temporary table with same schema as V1
        conn = duckdb.connect(":memory:")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS v1 (
                REF_DATE TIMESTAMP,
                TARGET INTEGER,
                SEXO CHAR(1),
                IDADE FLOAT,
                VAR4 CHAR(1),
                ESTADO CHAR(2),
                CLASSE CHAR(1)
            )
        """
        )
        # Test query syntax
        conn.execute(f"EXPLAIN {sql}")
        return True
    except Exception as e:
        print(f"[check_sql_syntax] Error: {e}")
        return False
    finally:
        conn.close()


@tool
def execute_sql_query(sql: str) -> Dict:
    """
    Executa a query SQL e retorna os resultados.
    Args:
        sql: Query SQL a ser executada
    Retorna:
        Dict: Resultados da query em formato de dicionário
    """
    try:
        connector = DBConnector()
        results = connector.execute_query(sql)
        df = results
        if "REF_DATE" in df.columns:
            df["REF_DATE"] = pd.to_datetime(df["REF_DATE"])
        return {"data": df}

    except Exception as e:
        print(f"[execute_sql_query] Error: {e}")
        return {"error": str(e)}


class SQLExecutor:
    """Lida com a geração e execução de queries SQL usando LLM."""

    def __init__(self):
        self.llm = ChatOpenAI(temperature=0, model=OPENAI_MODEL, api_key=OPENAI_API_KEY)
        self.sql_prompt = PromptTemplate.from_template(
            template=SQL_GENERATOR_TEMPLATE
        ).partial(db_schema=TABLE_INFO)
        self.parser = SQLQueryOutputParser()

    def generate_sql_query(self, user_input: str) -> str:
        """
        Gera uma query SQL a partir do input do usuário usando LLM.
        Args:
            user_input: Consulta em linguagem natural
        Retorna:
            str: Query SQL gerada
        """
        try:
            prompt_text = self.sql_prompt.format(user_input=user_input)
            response = self.llm.invoke(prompt_text)
            sql_query = self.parser.parse(response.content)
            return sql_query
        except Exception as e:
            raise ValueError(f"Failed to generate SQL query: {str(e)}")

    def run(self, user_input: str) -> Dict:
        """
        Mét odo principal do agente.
        1. Gera a query SQL a partir do input do usuário.
        2. Valida a sintaxe da query usando a tool check_sql_syntax.
        3. Se válida, executa a query usando a tool execute_sql_query.
        4. Retorna a query e os resultados.
        """
        # Passo 1: Gera a query SQL
        sql_query = self.generate_sql_query(user_input)

        # Passo 2: Checa a sintaxe da query
        syntax_valid = check_sql_syntax.invoke({"sql": sql_query})
        print(f"\n[Sintaxe SQL válida?] {syntax_valid}")

        if not syntax_valid:
            return {"error": "A sintaxe SQL gerada é inválida."}

        # Passo 3: Executa a query e obtém os resultados em JSON
        query_result = execute_sql_query.invoke({"sql": sql_query})
        print("\n=== Resultado da Consulta ===")
        print(query_result)

        # Passo 4: Retorna o resultado final
        final_response = {"sql_query": sql_query, "data": query_result["data"]}
        return final_response

if __name__ == "__main__":
    try:
        input_query = "Qual a média de idade por estado?"
        executor = SQLExecutor()
        result = executor.run(input_query)
        print("\n=== Final Response ===")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
