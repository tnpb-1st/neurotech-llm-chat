import pandas
import pandas as pd
from langchain_core.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from config.constants import OPENAI_MODEL, OPENAI_API_KEY, TABLE_INFO, INSIGHT_FAIL_MSG
from src.llms.prompts.prompts import INSIGHTS_GENERATOR_TEMPLATE
from src.llms.parsers.insights_output_parser import InsightsOutputParser


class InsightsGenerator:
    """
    Agente responsável por gerar insights a partir de uma pergunta do usuário, da query SQL executada
    e dos dados retornados.
    """

    def __init__(self):
        # Inicializa o LLM com o modelo configurado
        self.llm = ChatOpenAI(temperature=0, model=OPENAI_MODEL, api_key=OPENAI_API_KEY)
        # Cria o prompt template, injetando o contexto do banco (TABLE_INFO)
        self.prompt = PromptTemplate.from_template(
            template=INSIGHTS_GENERATOR_TEMPLATE
        ).partial(db_schema=TABLE_INFO)
        self.output_parser = InsightsOutputParser()

    def generate_insights(self, input_dict: dict) -> str:
        """
        Gera insights a partir dos dados fornecidos.

        Args:
            input_dict (dict): Dicionário contendo:
                - 'input': a pergunta do usuário;
                - 'sql_query': a query SQL executada;
                - 'data': os dados retornados (por exemplo, uma representação textual ou JSON do dataframe).

        Returns:
            str: Texto com os insights gerados.
        """
        if (
            not input_dict
            or "error" in input_dict
            or ("data" in input_dict and len(input_dict["data"]) == 0)
        ):
            return INSIGHT_FAIL_MSG
        try:
            dataframe = str(input_dict["data"])
            if type(input_dict["data"]) == pd.DataFrame:
                dataframe = str(input_dict["data"].to_json())
            # Formata o prompt preenchendo o input_dict no template
            prompt_text = self.prompt.format(
                user_query=str(input_dict["input"]),
                sql_query=str(input_dict["sql_query"]),
                dataframe=dataframe,
            )
            # Chama o LLM com o prompt formatado
            response = self.llm.invoke(prompt_text)
            # Retorna o conteúdo da resposta (insights)
            parsed_response = self.output_parser.parse(response.content)
            return parsed_response
        except Exception as e:
            raise ValueError(f"Falha ao gerar insights: {str(e)}")


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo de dados de entrada
    input_data = {
        "input": "Qual a média de idade por estado?",
        "sql_query": (
            "SELECT ESTADO, AVG(IDADE) as media_idade FROM V1 "
            "WHERE IDADE IS NOT NULL GROUP BY ESTADO ORDER BY ESTADO;"
        ),
        "data": "[{'ESTADO': 'SP', 'media_idade': 35.4}, {'ESTADO': 'RJ', 'media_idade': 33.2}, {'ESTADO': 'PE', 'media_idade': 36.8}]",
    }

    insights_agent = InsightsGenerator()
    insights = insights_agent.generate_insights(input_data)
    print("Insights gerados:")
    print(insights)
