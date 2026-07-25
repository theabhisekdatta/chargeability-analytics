import os
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from sqlalchemy import text


load_dotenv()


class SQLTOOL:

    def __init__(self):
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=self.GROQ_API_KEY,
            temperature=0
        )
        self.db = SQLDatabase.from_uri(
            "postgresql+psycopg2://"
            f"{os.getenv('POSTGRES_USER')}:"
            f"{os.getenv('POSTGRES_PASSWORD')}@"
            f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
            f"{os.getenv('POSTGRES_PORT', '5432')}/"
            f"{os.getenv('POSTGRES_DB', 'chargeability_db')}"
        )

    def generate_sql(self, question: str):
        schema = self.db.get_table_info()
        prompt = f"""
        You are an expert PostgreSQL SQL developer.

        You have access to the following database schema:

        {schema}

        Convert the user's natural language question into a PostgreSQL SQL query.

        Rules:
        1. Generate only SELECT statements.
        2. Do not use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, or CREATE.
        3. Use only tables and columns that exist in the schema.
        4. Use proper JOIN conditions based on foreign keys.
        5. Do not invent columns.
        6. Return only the SQL query.
        7. Use PostgreSQL syntax.

        User question:
        {question}
        """
        response = self.llm.invoke(prompt)
        return response.content

    def clean_sql(self, sql: str) -> str:
        sql = sql.strip()
        if sql.startswith("```sql"):
            sql = sql[len("```sql"):]
        elif sql.startswith("```"):
            sql = sql[len("```"):]
        if sql.endswith("```"):
            sql = sql[:-3]
        return sql.strip()


    def execute_sql(self, sql: str):
        sql = self.clean_sql(sql)
        with self.db._engine.connect() as connection:
            result = connection.execute(text(sql))
            rows = result.fetchall()
            return rows