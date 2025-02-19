import unittest
from src.config.constants import OPENAI_API_KEY, OPENAI_MODEL, TABLE_INFO
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.llms.prompts.prompts import QUERY_VALIDATOR_TEMPLATE
from dotenv import load_dotenv
import os


DB_SCHEMA = TABLE_INFO


class QueryValidator:
    def __init__(self):
        # Inicializa o modelo gpt-4o-mini
        self.llm = ChatOpenAI(
            model=OPENAI_MODEL,  # modelo configurado para seu ambiente
            temperature=0,
            api_key=OPENAI_API_KEY
        )
        # Cria o template do prompt
        self.prompt = ChatPromptTemplate.from_template(QUERY_VALIDATOR_TEMPLATE)
        # Concatena o prompt com a LLM para formar a chain
        self.chain = self.prompt | self.llm

    def validate_query(self, user_input: str) -> str:
        """
        Valida se a query/pergunta do usuário pode ser respondida com os dados disponíveis.
        Realiza uma chamada real para a LLM.

        Args:
            user_input (str): Query ou pergunta do usuário

        Returns:
            str: 'valid' ou 'invalid'
        """
        try:
            response = self.chain.invoke({
                "db_schema": DB_SCHEMA,
                "user_input": user_input
            })
            return response.content.strip().lower()
        except Exception as e:
            print(f"Erro ao processar a query: {e}")
            return "invalid"

class TestQueryValidatorIntegration(unittest.TestCase):
    def setUp(self):
        # Inicializa o validador com chamada real para a LLM
        self.validator = QueryValidator()

    def test_valid_query_average_age_by_state(self):
        query = "Qual a média de idade por estado?"
        result = self.validator.validate_query(query)
        print(f"\nQuery: {query}\nResultado: {result}")
        self.assertEqual(result, "valid")

    def test_invalid_query_delete(self):
        query = "DELETE FROM tabela WHERE idade > 30"
        result = self.validator.validate_query(query)
        print(f"\nQuery: {query}\nResultado: {result}")
        self.assertEqual(result, "invalid")

    def test_invalid_query_salary_by_class(self):
        query = "Qual o salário médio por classe?"
        result = self.validator.validate_query(query)
        print(f"\nQuery: {query}\nResultado: {result}")
        self.assertEqual(result, "invalid")

    def test_valid_query_female_count_by_state(self):
        query = "Quantas pessoas do sexo feminino tem em cada estado?"
        result = self.validator.validate_query(query)
        print(f"\nQuery: {query}\nResultado: {result}")
        self.assertEqual(result, "valid")

    def test_valid_query_select(self):
        query = "SELECT idade, estado FROM v1 WHERE sexo = 'F'"
        result = self.validator.validate_query(query)
        print(f"\nQuery: {query}\nResultado: {result}")
        self.assertEqual(result, "valid")

    def test_invalid_query_update(self):
        query = "UPDATE tabela SET idade = 30"
        result = self.validator.validate_query(query)
        print(f"\nQuery: {query}\nResultado: {result}")
        self.assertEqual(result, "invalid")

if __name__ == "__main__":
    unittest.main()