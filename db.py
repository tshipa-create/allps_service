from datetime import datetime, timezone
import config
import pandas as pd
from app_logging import logObject
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from sqlalchemy.pool import QueuePool


def get_snowflake_engine():
    engine = create_engine(
        URL(account=config.SF_ACCOUNT, user=config.SF_USER, password=config.SF_PASSWORD, database=config.SF_DATABASE),
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=3600,
    )
    return engine


def process_df(df: pd.DataFrame):
    df.columns = df.columns.str.upper()
    return df


def fetch_retry_loans_data():
    sql_query = """
                SELECT * FROM PLANET42_LIVE_DB.DATA_TEAM.VIEW_ALLPS_RETRY_INSTALMENTS
                ORDER BY INST_NUM  DESC
                """
    try:
        engine = get_snowflake_engine()
        with engine.connect() as sf_connection:
            df = pd.read_sql(sql_query, sf_connection)
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
            datetime.now(timezone.utc),
            config.ALLPS_HOST,
            method_name,
            resp_code,
            resp_msg,
            request_xml,
            response_xml,
        )
        engine = get_snowflake_engine()
        with engine.connect() as sf_connection:
            result = sf_connection.execute(insert_sql, data)
            logObject.warning(
                "Row %d inserted into Snowflake table: %s", result.rowcount, config.SF_ALLPS_XML_LOG_TABLE
            )
    except Exception as e:
        logObject.error("Error saving ALLPS response to Snowflake: %s", e)


def fetch_daily_monitoring_data():
    logObject.warning("Fetching daily monitoring data from Snowflake...")
    sql_query = """
                SELECT
                    CURRENT_DATE() AS MONITORING_DATE,
                    COUNT(ID) AS COUNT_OF_ROWS,
                    HOST,
                    METHOD_NAME ,
                    RESPONSE_CODE ,
                    RESPONSE_MESSAGE
                FROM
                    PLANET42_LIVE_DB.DATA_TEAM.ALLPS_SERVICE_API_LOGS
                WHERE
                    REQUEST_DATE_UTC::DATE = CURRENT_DATE()
                GROUP BY
                    HOST,
                    METHOD_NAME ,
                    RESPONSE_CODE ,
                    RESPONSE_MESSAGE
                """
    try:
        engine = get_snowflake_engine()
        with engine.connect() as sf_connection:
            df = pd.read_sql(sql_query, sf_connection)
            logObject.warning("Found %d rows of daily monitoring data", len(df))
            return process_df(df)
    except Exception as e:
        logObject.error("Error fetching daily monitoring data: %s", e)
        return None
