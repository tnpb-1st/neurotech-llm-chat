import unittest
from src.llms.agents.sql_executor import SQLExecutor


class TestSQLExecutor(unittest.TestCase):
    def setUp(self):
        # Inicializa uma instância do agente
        self.executor = SQLExecutor()

    def test_basic_average_by_state(self):
        self.executor.generate_sql_query = lambda user_input: (
            "SELECT ESTADO, AVG(IDADE) as media_idade FROM V1 "
            "WHERE IDADE IS NOT NULL GROUP BY ESTADO ORDER BY ESTADO;"
        )
        result = self.executor.run("Qual a média de idade por estado?")
        self.assertNotIn("error", result)
        print("\nTeste média por estado - Resultado:", result)

    def test_complex_age_distribution(self):
        # Análise complexa de distribuição de idade por classe e sexo
        self.executor.generate_sql_query = lambda user_input: (
            "SELECT CLASSE, SEXO, "
            "COUNT(*) as total, "
            "AVG(IDADE) as media_idade, "
            "MIN(IDADE) as idade_min, "
            "MAX(IDADE) as idade_max, "
            "PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY IDADE) as mediana_idade "
            "FROM V1 "
            "WHERE CLASSE IS NOT NULL AND SEXO IS NOT NULL "
            "GROUP BY CLASSE, SEXO "
            "ORDER BY CLASSE, SEXO;"
        )
        result = self.executor.run(
            "Qual a distribuição de idade por classe e sexo, incluindo média, mínimo, máximo e mediana?"
        )
        self.assertNotIn("error", result)
        print("\nTeste distribuição complexa - Resultado:", result)

    def test_temporal_analysis(self):
        # Análise temporal com agregações mensais
        self.executor.generate_sql_query = lambda user_input: (
            "SELECT "
            "DATE_TRUNC('month', REF_DATE) as mes, "
            "ESTADO, "
            "COUNT(*) as total_registros, "
            "AVG(IDADE) as media_idade, "
            "COUNT(CASE WHEN TARGET = 1 THEN 1 END) as total_target_positivo "
            "FROM V1 "
            "WHERE ESTADO IS NOT NULL "
            "GROUP BY DATE_TRUNC('month', REF_DATE), ESTADO "
            "ORDER BY mes, ESTADO;"
        )
        result = self.executor.run(
            "Como variam os registros, média de idade e total de target positivo por mês e estado?"
        )
        self.assertNotIn("error", result)
        print("\nTeste análise temporal - Resultado:", result)

    def test_class_distribution_by_age_groups(self):
        # Distribuição de classes por faixas etárias
        self.executor.generate_sql_query = lambda user_input: (
            "SELECT "
            "CASE "
            "   WHEN IDADE < 25 THEN 'Jovem' "
            "   WHEN IDADE < 45 THEN 'Adulto' "
            "   ELSE 'Senior' "
            "END as faixa_etaria, "
            "CLASSE, "
            "COUNT(*) as total, "
            "ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY CLASSE), 2) as percentual "
            "FROM V1 "
            "WHERE IDADE IS NOT NULL AND CLASSE IS NOT NULL "
            "GROUP BY "
            "CASE "
            "   WHEN IDADE < 25 THEN 'Jovem' "
            "   WHEN IDADE < 45 THEN 'Adulto' "
            "   ELSE 'Senior' "
            "END, "
            "CLASSE "
            "ORDER BY CLASSE, faixa_etaria;"
        )
        result = self.executor.run(
            "Qual a distribuição percentual das classes por faixas etárias (jovem, adulto, senior)?"
        )
        self.assertNotIn("error", result)
        print("\nTeste distribuição por faixa etária - Resultado:", result)

    def test_target_analysis_with_window_functions(self):
        # Análise complexa de TARGET usando funções de janela
        self.executor.generate_sql_query = lambda user_input: (
            "SELECT "
            "ESTADO, "
            "CLASSE, "
            "COUNT(*) as total_registros, "
            "SUM(TARGET) as total_positivos, "
            "ROUND(AVG(TARGET) * 100, 2) as taxa_positivos, "
            "ROUND(AVG(TARGET) * 100 - "
            "LAG(ROUND(AVG(TARGET) * 100, 2)) OVER (PARTITION BY ESTADO ORDER BY CLASSE), 2) "
            "as variacao_classe_anterior "
            "FROM V1 "
            "WHERE ESTADO IS NOT NULL AND CLASSE IS NOT NULL "
            "GROUP BY ESTADO, CLASSE "
            "ORDER BY ESTADO, CLASSE;"
        )
        result = self.executor.run(
            "Qual a análise de TARGET por estado e classe, incluindo variação entre classes?"
        )
        self.assertNotIn("error", result)
        print("\nTeste análise TARGET - Resultado:", result)

    def test_complex_gender_analysis(self):
        # Análise complexa de distribuição por sexo com subconsultas
        self.executor.generate_sql_query = lambda user_input: (
            "WITH stats_by_state AS ( "
            "   SELECT "
            "       ESTADO, "
            "       SEXO, "
            "       COUNT(*) as total, "
            "       AVG(IDADE) as media_idade, "
            "       SUM(TARGET) as total_target "
            "   FROM V1 "
            "   WHERE ESTADO IS NOT NULL AND SEXO IS NOT NULL "
            "   GROUP BY ESTADO, SEXO "
            "), "
            "state_totals AS ( "
            "   SELECT "
            "       ESTADO, "
            "       SUM(total) as total_estado "
            "   FROM stats_by_state "
            "   GROUP BY ESTADO "
            ") "
            "SELECT "
            "   s.ESTADO, "
            "   s.SEXO, "
            "   s.total, "
            "   ROUND(s.total * 100.0 / t.total_estado, 2) as percentual_estado, "
            "   s.media_idade, "
            "   ROUND(s.total_target * 100.0 / s.total, 2) as taxa_target "
            "FROM stats_by_state s "
            "JOIN state_totals t ON s.ESTADO = t.ESTADO "
            "ORDER BY s.ESTADO, s.SEXO;"
        )
        result = self.executor.run(
            "Qual a análise detalhada da distribuição por sexo em cada estado, "
            "incluindo percentuais, média de idade e taxa de target?"
        )
        self.assertNotIn("error", result)
        print("\nTeste análise por sexo - Resultado:", result)


if __name__ == "__main__":
    unittest.main()
