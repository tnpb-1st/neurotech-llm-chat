import re
from langchain.schema import BaseOutputParser, OutputParserException


class InsightsOutputParser(BaseOutputParser):
    def parse(self, text: str) -> str:
        """
        Extrai o texto que vem após '**Insights**:' na resposta.

        Args:
            text (str): A resposta completa contendo a seção de insights.

        Returns:
            str: O texto dos insights, com espaços e quebras de linha indesejados removidos.

        Raises:
            OutputParserException: Se não for possível extrair os insights.
        """
        match = re.search(r"\*\*Insights\*\*:\s*(.*)", text, re.DOTALL)
        if match:
            insights = match.group(1).strip(" \n")
            return insights
        else:
            raise OutputParserException(
                "Não foi possível extrair os insights da resposta."
            )

    @property
    def _type(self) -> str:
        return "insights_output_parser"
