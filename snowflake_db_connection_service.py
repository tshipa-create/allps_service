from sqlalchemy import create_engine
from snowflake.connector.pandas_tools import pd_writer
from app_logging import logObject
import pandas as pd
from snowflake.connector.errors import OperationalError
from requests.exceptions import ConnectionError as RequestsConnectionError


class SnowflakeConnectionManager:
    """Manages Snowflake connections using SQLAlchemy."""

    def __init__(self, user: str, password: str, account: str, database: str):
        self.connection = SnowflakeConnectionWithSqlalchemy(user, password, account, database)

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class SnowflakeConnectionWithSqlalchemy:
    """
    A class for establishing a connection to Snowflake using SQLAlchemy.
    """

    def __init__(self, user: str, password: str, account: str, database: str):
        self.user = user
        self.password = password
        self.account = account
        self.database = database
        try:
            logObject.warning("Creating Snowflake connection")
            self.engine = create_engine(f"snowflake://{self.user}:{self.password}@{self.account}/{self.database}")
            self.snowflake_connection = self.engine.connect()
            logObject.warning("Snowflake connection established")
        except Exception as e:
            msg = f"Exception occured: {e}, when establishing Snowflake connection"
            logObject.error(msg)

    def retry_connection(self):
        try:
            self.snowflake_connection = self.engine.connect()
            logObject.warning("Snowflake connection re-established")
            return self.snowflake_connection
        except Exception as e:
            msg = f"Exception occurred: {e}, when re-establishing Snowflake connection"
            logObject.error(msg)
            return None

    def retry_execute(self, func, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except (OperationalError, RequestsConnectionError):
            logObject.error("Connection to Snowflake database lost, reconnecting...")
            self.snowflake_connection = self.retry_connection()
            if self.snowflake_connection:
                logObject.warning("Reconnected to Snowflake database, re-executing function...")
                result = func(*args, **kwargs)
                return result
            return None
        except Exception as e:
            msg = f"Exception occurred: {e}"
            logObject.error(msg)
            return None

    def execute_sql_query(self, query: str):
        try:
            result = self.retry_execute(self.snowflake_connection.execute, query)
            logObject.warning(
                "Query executed successfully with %d row(s) and query type: %s",
                result.rowcount,
                query[0:7],
            )
            return result
        except Exception as e:
            msg = f"Exception occured: {e}, when executing query"
            logObject.error(msg)

    def create_table_and_insert_data(
        self,
        df: pd.DataFrame,
        schema: str,
        table_name: str,
        if_exists: str,
        chunksize=None,
    ):
        try:
            self.snowflake_connection.execute(f"USE SCHEMA {self.database}.{schema}")
            if if_exists == "replace":
                logObject.warning('Rewriting table "%s" to Snowflake database', table_name)
            elif if_exists == "append":
                logObject.warning(
                    'Appending rows to table "%s" to Snowflake schema: "%s"',
                    table_name,
                    schema,
                )
            else:
                logObject.error('Unknown if_exists type: "%s"', if_exists)

            def insert_data():
                df.to_sql(
                    con=self.snowflake_connection,
                    name=table_name.lower(),
                    schema=schema,
                    if_exists=if_exists,
                    index=False,
                    chunksize=chunksize,
                    method=pd_writer,
                )

            self.retry_execute(insert_data)
            logObject.warning(
                'Rows inserted to Snowflake schema: "%s" and table: "%s"',
                schema,
                table_name,
            )
        except Exception as e:
            msg = f"Exception occured: {e}, when inserting data to Snowflake"
            logObject.error(msg)

    def read_into_dataframe(self, query: str):
        try:
            df = pd.read_sql(query, self.snowflake_connection)
            logObject.warning("Reading SQL SELECT query into DataFrame")
            return df
        except Exception as e:
            msg = f"Exception occured: {e}, when reading into DataFrame"
            logObject.error(msg)

    def close(self):
        try:
            self.snowflake_connection.close()
            logObject.warning("Snowflake connection closed")
        except Exception as e:
            msg = f"Exception occured: {e}, when closing Snowflake connection"
            logObject.error(msg)
