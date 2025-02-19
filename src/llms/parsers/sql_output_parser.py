from langchain.schema import BaseOutputParser, OutputParserException
import re


class SQLQueryOutputParser(BaseOutputParser):
    """Parser para extrair query SQL da resposta do LLM."""

    def parse(self, text: str) -> str:
        """
        Extrai a seção da query SQL da resposta do modelo.
        Args:
            text: Resposta bruta do modelo LLM
        Retorna:
            str: Query SQL extraída
        Levanta:
            OutputParserException: Se a query SQL não puder ser extraída
        """
        sql_pattern = (
            r"Query SQL:\s*(?:```sql)?\s*(.*?)\s*(?:```)?(?:Input do usuário:|$)"
        )
        sql_match = re.search(sql_pattern, text, re.DOTALL | re.IGNORECASE)
        if not sql_match:
            raise OutputParserException(
                "Could not extract SQL query from model response"
            )
        sql_query = sql_match.group(1).strip()
        return sql_query

    @property
    def _type(self) -> str:
        return "sql_query_output_parser"
