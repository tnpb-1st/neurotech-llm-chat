import unittest
from config.constants import COMPLEX_ADVERSARIAL_QUERY, TABLE_INFO
from src.llms.agents.query_validator import QueryValidator

DB_SCHEMA = TABLE_INFO


class TestQueryValidatorIntegration(unittest.TestCase):
    def setUp(self):
        # Inicializa o validador com chamada real para a LLM
        self.validator = QueryValidator()

    def test_valid_query_average_age_by_state(self):
        query = "Qual a média de idade por estado?"
        result = self.validator.validate_query(query)[0]
        print(f"\nQuery: {query}\nResultado: {result}")
        self.assertEqual(result, "valid")

    def test_invalid_query_delete(self):
        query = "DELETE FROM tabela WHERE idade > 30"
        result = self.validator.validate_query(query)[0]
        print(f"\nQuery: {query}\nResultado: {result}")
        self.assertEqual(result, "invalid")

    def test_invalid_query_salary_by_class(self):
        query = "Qual o salário médio por classe?"
        result = self.validator.validate_query(query)[0]
        print(f"\nQuery: {query}\nResultado: {result}")
        self.assertEqual(result, "invalid")

    def test_valid_query_female_count_by_state(self):
        query = "Quantas pessoas do sexo feminino tem em cada estado?"
        result = self.validator.validate_query(query)[0]
        print(f"\nQuery: {query}\nResultado: {result}")
        self.assertEqual(result, "valid")

    def test_valid_query_select(self):
        query = "SELECT idade, estado FROM v1 WHERE sexo = 'F'"
        result = self.validator.validate_query(query)[0]
        print(f"\nQuery: {query}\nResultado: {result}")
        self.assertEqual(result, "valid")

    def test_invalid_query_update(self):
        query = "UPDATE tabela SET idade = 30"
        result = self.validator.validate_query(query)[0]
        print(f"\nQuery: {query}\nResultado: {result}")
        self.assertEqual(result, "invalid")

    def test_complex_query(self):
        query = (
            'eu gostaria de saber quantos homens com mais de 18 anos presentes nos estados "PE", "PB" ou "SP" e '
            'que pertencem á classe "A" estão cadastrados no banco de dados entre os anos de 2017 e 2018'
        )
        result = self.validator.validate_query(query)[0]
        print(f"\nQuery: {query}\nResultado: {result}")
        self.assertEqual(result, "valid")

    def test_complex_adversarial_query(self):
        query = COMPLEX_ADVERSARIAL_QUERY
        result = self.validator.validate_query(query)[0]
        print(f"\nQuery: {query}\nResultado: {result}")
        self.assertEqual(result, "invalid")


if __name__ == "__main__":
    unittest.main()
