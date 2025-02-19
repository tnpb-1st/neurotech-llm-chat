import unittest
from src.llms.agents.sql_executor import SQLExecutor


class TestSQLExecutor(unittest.TestCase):
    def setUp(self):
        # Inicializa uma instância do agente
        self.executor = SQLExecutor()

    def test_valid_query(self):
        # Simula a geração de uma query SQL válida
        self.executor.generate_sql_query = lambda user_input: (
            "SELECT ESTADO, AVG(IDADE) as media_idade FROM V1 "
            "WHERE IDADE IS NOT NULL GROUP BY ESTADO ORDER BY ESTADO;"
        )
        # Chama o agente com um input de consulta válido
        result = self.executor.run("Qual a média de idade por estado?")
        # Para uma query válida, o dicionário retornado NÃO deve conter a key "error"
        self.assertNotIn(
            "error", result, "A query válida não deveria retornar 'error'."
        )
        print("\nTeste válido - Resultado:", result)


if __name__ == "__main__":
    unittest.main()
