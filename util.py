from datetime import datetime, timezone
import pandas as pd
import xmltodict
from logger_config import logger


def get_reply_code_and_message(xml_response: str, method_name: str):
    response_dict = xmltodict.parse(xml_response)
    reply_code = response_dict["responses"][method_name]["reply_cd"]
    reply_message = response_dict["responses"][method_name]["reply_str"]
    return reply_code, reply_message


def format_date_to_string(date: datetime):
    return date.strftime("%Y%m%d")


def is_auth_guid(guid: str) -> bool:
    if guid is None:
        logger.exception("Authentication failed. Cannot proceed with get_instalment")
        return False
    return True


def check_instalment_status(current_status: str, check_status: str) -> bool:
    if current_status == check_status:
        logger.info(f"Instalment status as expected: {check_status}")
        return True
    logger.warning(
        f"Instalment status not as expected, current_status: {current_status}, check_status: {check_status}"
    )
    return False


def check_instalment_not_in_future(instalment_date: str) -> bool:
    if instalment_date is None:
        logger.exception("Instalment date is None. ")
        return False
    current_utc_date = datetime.now(timezone.utc).date()
    installment_as_date = datetime.strptime(instalment_date, "%Y%m%d").date()
    if installment_as_date > current_utc_date:
        logger.warning(
            f"Instalment date is in future: {instalment_date} with current date: {current_utc_date}"
        )
        return False
    return True


def validate_full_instalment_info(
    current_status: str, check_status: str, instalment_date: str
) -> bool:
    status_valid = check_instalment_status(current_status, check_status)
    date_valid = check_instalment_not_in_future(instalment_date)
    return status_valid and date_valid


def installments_statistics_from_processings(
    total_instalments: int, edited_instalments: int
):
    if total_instalments == 0:
        logger.warning("RUN STATISTICS: No instalments to edit")
    elif total_instalments == edited_instalments:
        logger.info("RUN STATISTICS: All instalments were edited")
    elif total_instalments != edited_instalments:
        logger.warning(
            f"RUN STATISTICS: Mismatch between total instalments: {total_instalments} and edited instalments: {edited_instalments}"
        )


def normalize_xml(xml_str: str):
    return "".join(xml_str.split())


def check_loans_data_fetch(df):
    if df is None:
        logger.exception("Error fetching retry loans data. Exiting process...")
        return False
    elif df.empty:
        logger.warning("No filtered retry loans data found. Exiting process...")
        return False
    return True


def add_tz_to_df_date_cols(df: pd.DataFrame):
    df.columns = df.columns.str.upper()
    for column in df.columns:
        if (
            df[column].dtype == "datetime64[ns]"
        ):  # add timezone to datetime columns, so they would be saved correctly in Snowflake
            try:
                df[column] = pd.to_datetime(
                    df[column], format="%Y-%m-%d %H:%M:%S.%f", utc=True
                )
                logger.info(
                    f'Successfully converted column "{column}" to datetime with timezone'
                )
            except Exception as e:
                logger.error(f"Error converting column {column} to datetime: {e}")
    return df


# CNT_PCT - share of total retries to process
# AMT_PCT - share of total instalment amount to retry
def add_split_info_cols(df: pd.DataFrame):

    split_cfg = [
        {"cnt_pct": 50, "amt_pct": 100},
        {"cnt_pct": 50, "amt_pct": 50},
    ]

    df["CNT_PCT"] = None
    df["AMT_PCT"] = None

    size = len(df)
    i = 0

    for si, spl in enumerate(split_cfg):
        cnt_pct = spl["cnt_pct"]
        amt_pct = spl["amt_pct"]
        cnt = int(size * cnt_pct / 100)

        # last split takes remaining
        if si == len(split_cfg) - 1:
            df.loc[i:, "CNT_PCT"] = cnt_pct
            df.loc[i:, "AMT_PCT"] = amt_pct
        else:
            df.loc[i : i + cnt, "CNT_PCT"] = cnt_pct
            df.loc[i : i + cnt, "AMT_PCT"] = amt_pct

        i += cnt
