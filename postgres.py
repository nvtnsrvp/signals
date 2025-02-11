import contextlib
import psycopg2

import config

class PostgresConnection:
    """Manages a connection to a PostgreSql database using psycopg2."""

    def __init__(self):
        self.config = {
            'host': config.host,
            'dbname': config.dbname,
            'user': config.user,
            'password': config.password
            }
        self.connect()

    def connect(self) -> None:
        """Connect to the database."""
        self.conn = psycopg2.connect(**self.config)

    def init_database(self) -> None:
        """Initialize the database."""
        create_runs_table_query = """
            CREATE TABLE IF NOT EXISTS runs (
                run_id SERIAL PRIMARY KEY,
                limit INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_runs_run_id ON runs(run_id);
            CREATE INDEX IF NOT EXISTS idx_runs_created_at ON runs(created_at);
        """
        # TODO: See if we need created_at, given that run and fetch times are different.
        create_mentions_table_query = """
            CREATE TABLE IF NOT EXISTS mentions (
                author VARCHAR(50) NOT NULL,
                id VARCHAR(50) NOT NULL,
                run_id INTEGER NOT NULL,
                symbol VARCHAR(50) NOT NULL,
                is_submission BOOLEAN NOT NULL,
                PRIMARY KEY (id, is_submission, run_id, symbol)
            );
            CREATE INDEX IF NOT EXISTS idx_mentions_symbols ON mentions(symbol);
        """

        with self.conn.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(create_runs_table_query)
                cursor.execute(create_mentions_table_query)
                conn.commit()
                print("Database initialized")

    def execute_run(self, lmit: int) -> int:
        insert_run_id_query = """
            INSERT INTO runs (limit) VALUES (%s) RETURNING run_id;
        """
        with self.conn.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_run_id_query)
                row = cursor.fetchone()
                if row:
                    return row[0]