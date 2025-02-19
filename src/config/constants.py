import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"
TABLE_INFO = [
    {
        "Nome": "REF_DATE",
        "Tipo do Dado": "TIMESTAMP WITH TIME ZONE",
        "Exemplo": "2017-06-01 00:00:00+00:00",
    },
    {"Nome": "TARGET", "Tipo do Dado": "INT (0 or 1)", "Exemplo": "0, 1"},
    {"Nome": "SEXO", "Tipo do Dado": "CHAR(1) or NULL", "Exemplo": "M, F, NULL"},
    {
        "Nome": "IDADE",
        "Tipo do Dado": "FLOAT or NULL",
        "Exemplo": "34.137, 40.447, NULL",
    },
    {"Nome": "VAR4", "Tipo do Dado": "CHAR(1) or NULL", "Exemplo": "S, NULL"},
    {
        "Nome": "ESTADO",
        "Tipo do Dado": "CHAR(2) or NULL",
        "Exemplo": "PE, PB, SP, RJ, NULL",
    },
    {"Nome": "CLASSE", "Tipo do Dado": "CHAR(1) or NULL", "Exemplo": "A, D, E, NULL"},
]
