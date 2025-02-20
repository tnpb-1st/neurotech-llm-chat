from typing import Dict
import re

from langchain import hub
from langchain.tools import Tool, tool
from langchain_openai import ChatOpenAI
from config.constants import OPENAI_API_KEY
from langchain_core.agents import AgentAction, AgentFinish


# Ferramentas
@tool
def check_sql_syntax(sql: str) -> bool:
    """This tool checks if the SQL syntax is valid by running the query in a
    DuckDB with a table like the real table. It returns True if the syntax is
    valid, otherwise it returns False."""
    print("[check_sql_syntax] Verificando sintaxe:", sql)
    return True


@tool
def execute_sql_query(sql: str) -> Dict:
    print("[execute_sql_query] Executando SQL:", sql)
    return {"data": [{"ESTADO": "SP", "media_idade": 35.4}]}


def main():
    # 1. Puxa o chain ReAct do Hub (implementação do hwchase17/react)
    react_chain = hub.pull("hwchase17/react")

    # 2. Configura o LLM (aqui utilizamos o ChatOpenAI, configurado com o modelo desejado)
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o-mini",  # ou outro modelo disponível
        api_key=OPENAI_API_KEY,
    )

    # 3. Define a lista de ferramentas que o agente poderá utilizar
    tools = [check_sql_syntax, execute_sql_query]

    # 4. Configura o chain injetando o LLM e as ferramentas
    react_chain = react_chain.configure(llm=llm, tools=tools)

    # 5. Define a pergunta do usuário (por exemplo, gerando uma query SQL para análise de dados)
    question = "Qual a média de idade por estado?"

    # 6. Chama o chain ReAct com a pergunta; o fluxo interno (Thought, Action, Observation, Final Answer)
    # é gerenciado pelo chain do Hub.
    result = react_chain(question)

    # 7. Exibe a resposta final
    print("Resposta final do agente ReAct:", result)


if __name__ == "__main__":
    main()
