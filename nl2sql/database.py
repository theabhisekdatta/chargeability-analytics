import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()


class Database:
    def __init__(self):
        self.host = os.getenv("POSTGRES_HOST", "localhost")
        self.port = os.getenv("POSTGRES_PORT", "5432")
        self.database = os.getenv("POSTGRES_DB", "chargeability_db")
        self.username = os.getenv("POSTGRES_USER", "postgres")
        self.password = os.getenv("POSTGRES_PASSWORD")

        self.connection_string = (
            f"postgresql+psycopg2://"
            f"{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )

        self.engine = create_engine(self.connection_string)

    def test_connection(self):
        with self.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return result.scalar() == 1