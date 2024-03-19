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


def fetch_retry_loans_data():
    sql_query = """
                SELECT * FROM PLANET42_LIVE_DB.DATA_TEAM.VIEW_ALLPS_RETRY_INSTALMENTS
                WHERE PROMISSORY_ID = '00052382B7'
                ORDER BY INST_NUM  DESC
                """
    try:
        with setup_snowflake_connection() as sf_connection:
            df = sf_connection.read_into_dataframe(sql_query)
            logObject.warning("Found %d retry loans data", len(df))
            return process_df(df)
    except Exception as e:
        logObject.error("Error fetching retry loans data: %s", e)
        return None


def save_allps_response_to_snowflake(
    resp_code: str, resp_msg: str, method_name: str, request_xml: str, response_xml: str
):
    try:
        insert_sql = f"""INSERT INTO {config.SF_SCHEMA}.{config.SF_ALLPS_XML_LOG_TABLE}
        (
            REQUEST_DATE_UTC,
            HOST,
            METHOD_NAME,
            RESPONSE_CODE,
            RESPONSE_MESSAGE,
            REQUEST_XML,
            RESPONSE_XML
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s
        )
        """
        data = (
            datetime.utcnow(),
            config.ALLPS_HOST,
            method_name,
            resp_code,
            resp_msg,
            request_xml,
            response_xml,
        )
        with setup_snowflake_connection() as sf_connection:
            sf_connection.insert_into_table(insert_sql, data, config.SF_ALLPS_XML_LOG_TABLE)
    except Exception as e:
        logObject.error("Error saving ALLPS response to Snowflake: %s", e)
