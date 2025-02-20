from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config.constants import TABLE_INFO, OPENAI_API_KEY, OPENAI_MODEL
from ..prompts.prompts import QUERY_VALIDATOR_TEMPLATE
from typing import Tuple
from config.constants import TABLE_NAME

# chamada
# validator = QueryValidator()
# validator.validate_query(query)


class QueryValidator:
    def __init__(self):

        self.llm = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=0,
            api_key=OPENAI_API_KEY,
        )

        # Cria o template do prompt
        self.prompt = ChatPromptTemplate.from_template(QUERY_VALIDATOR_TEMPLATE)

        # Cria a chain
        self.chain = self.prompt | self.llm

    def validate_query(self, user_input: str) -> Tuple[str, str]:
        """
        Valida se a query/pergunta do usuário pode ser respondida com os dados disponíveis

        Args:
            user_input (str): Query ou pergunta do usuário

        Returns:
            str: 'valid' ou 'invalid'
        """
        try:
            response = self.chain.invoke(
                {
                    "db_schema": TABLE_INFO,
                    "user_input": user_input,
                    "table_name": TABLE_NAME,
                }
            )
            reason, status = response.content.split("|")
            reason = reason.strip(" '\".[]")
            status = status.strip().capitalize()
            return reason, status
        except Exception as e:
            return "invalid", f"Erro {e} ao processar a query"
