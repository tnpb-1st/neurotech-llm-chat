import pandas as pd
import psycopg2

from config.constants import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
from ordered_set import OrderedSet


class DBConnector:
    def __init__(self):
        self.host = DB_HOST
        self.port = DB_PORT
        self.dbname = DB_NAME
        self.user = DB_USER
        self.password = DB_PASS

    def connect(self):
        """Establishes a connection to the database."""
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
        )

    def execute_query(self, query: str) -> pd.DataFrame:
        """Executes a SQL query and returns results if applicable."""
        result = pd.DataFrame()
        col_names = OrderedSet()
        try:
            conn = self.connect()
            with conn.cursor() as cur:
                cur.execute(query)
                for desc in cur.description:
                    col_names.add(str(desc.name).upper())
                if query.strip().upper().startswith("SELECT"):
                    df_data = cur.fetchall()
                    result = pd.DataFrame(df_data, columns=list(col_names))
                else:
                    conn.commit()
        finally:
            conn.close()
        return result
