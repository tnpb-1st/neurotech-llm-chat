import psycopg2
from ..config.constants import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

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
            password=self.password
        )

    def execute_query(self, query: str):
        """Executes a SQL query and returns results if applicable."""
        try:
            conn = self.connect()
            with conn.cursor() as cur:
                cur.execute(query)
                if query.strip().upper().startswith("SELECT"):
                    result = cur.fetchall()
                else:
                    conn.commit()
                    result = None
        finally:
            conn.close()
        return result
