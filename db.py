from datetime import datetime, timezone
import config
import pandas as pd
from logger_config import logger
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from sqlalchemy.pool import QueuePool
from snowflake.connector.pandas_tools import pd_writer
import util

# Global Engine
engine = create_engine(
    URL(
        account=config.SF_ACCOUNT,
        user=config.SF_USER,
        password=config.SF_PASSWORD,
        database=config.SF_DATABASE,
    ),
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
)


def fetch_raw_retry_loans_data():
    sql_query = f"""
                SELECT * FROM PLANET42_LIVE_DB.{config.SF_SCHEMA}.VIEW_ALLPS_RETRY_INSTALMENTS
                ORDER BY INST_NUM  DESC
                """
    try:
        with engine.connect() as sf_connection:
            df = pd.read_sql(sql_query, sf_connection)
            logger.info(
                f"Found {len(df)} raw retry loans data",
            )
            return util.add_tz_to_df_date_cols(df)
    except Exception as e:
        logger.exception(f"Error fetching raw retry loans data: {e}")
        return None


def save_results(df: pd.DataFrame, table_name: str):
    try:
        with engine.connect() as sf_connection:
            df.to_sql(
                table_name.lower(),
                sf_connection,
                schema=config.SF_SCHEMA,
                if_exists="append",
                index=False,
                method=pd_writer,
            )
            logger.info(
                f"Data saved to Snowflake table: {config.SF_SCHEMA}.{table_name}"
            )
    except Exception as e:
        logger.exception(f"Error saving data to Snowflake: {e}")


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
        with engine.connect() as sf_connection:
            result = sf_connection.execute(insert_sql, data)
            logger.info(
                f"Row {result.rowcount} inserted into Snowflake table: {config.SF_SCHEMA}.{config.SF_ALLPS_XML_LOG_TABLE}"
            )

    except Exception as e:
        logger.exception(f"Error saving ALLPS response to Snowflake: {e}")


def fetch_daily_monitoring_data():
    logger.info("Fetching daily monitoring data from Snowflake...")
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
        with engine.connect() as sf_connection:
            df = pd.read_sql(sql_query, sf_connection)
            logger.info(f"Found {len(df)} rows of daily monitoring data")
            return util.add_tz_to_df_date_cols(df)
    except Exception as e:
        logger.exception(f"Error fetching daily monitoring data: {e}")
        return None
