from datetime import datetime
import config
import snowflake_db_connection_service as snowflake_db
import pandas as pd
from app_logging import logObject


def setup_snowflake_connection():
    return snowflake_db.SnowflakeConnectionManager(
        account=config.SF_ACCOUNT,
        user=config.SF_USER,
        password=config.SF_PASSWORD,
        database=config.SF_DATABASE,
    )


def process_df(df: pd.DataFrame):
    df.columns = df.columns.str.upper()
    return df


def fetch_retry_loans_data():  # TODO: Change SQL to right one
    sql_query = """
    SELECT 1 FROM DUAL 
    """
    try:
        with setup_snowflake_connection() as sf_connection:
            df = sf_connection.read_into_dataframe(sql_query)
            return process_df(df)
    except Exception as e:
        logObject.error("Error fetching retry loans data: %s", e)
        return None


def save_allps_response_to_snowflake(resp_code: str, resp_msg: str, request_xml: str, response_xml: str):
    try:
        df = pd.DataFrame(
            [
                {
                    "REQUEST_DATE_UTC": datetime.utcnow(),
                    "HOST": config.ALLPS_HOST,
                    "RESPONSE_CODE": resp_code,
                    "RESPONSE_MESSAGE": resp_msg,
                    "REQUEST_XML": request_xml,
                    "RESPONSE_XML": response_xml,
                }
            ]
        )
        with setup_snowflake_connection() as sf_connection:
            sf_connection.create_table_and_insert_data(
                df=df, schema=config.SF_SCHEMA, table_name=config.SF_ALLPS_XML_LOG_TABLE, if_exists="append"
            )
    except Exception as e:
        logObject.error("Error saving ALLPS response to Snowflake: %s", e)
