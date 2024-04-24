import json
import pandas as pd
from logger_config import logger

DAYS_BEFORE_NEXT_INSTALMENT_FILTER = "DAYS_BEFORE_NEXT_INSTALMENT_FILTER"
DAYS_BEFORE_NEXT_INSTALMENT_FLAG = "DAYS_BEFORE_NEXT_INSTALMENT_FLAG"


def add_days_flag_to_include_logic_dict(include_logic: dict):
    # idea is that if the filter is more than 30 places, there is probably a filter logic input in config
    if len(include_logic[DAYS_BEFORE_NEXT_INSTALMENT_FILTER]) > 30:
        new_dict = {DAYS_BEFORE_NEXT_INSTALMENT_FLAG: True}
        new_dict.update(include_logic)
    else:
        new_dict = {DAYS_BEFORE_NEXT_INSTALMENT_FLAG: False}
        new_dict.update(include_logic)
    return new_dict


def calculate_days_before_next_instalment_flag(df: pd.DataFrame, include_logic: dict):
    modified_days_before_next_instalment_filter = include_logic[DAYS_BEFORE_NEXT_INSTALMENT_FILTER].replace(
        "DAYS_BEFORE_NEXT_INSTALMENT", "x"
    )
    if len(include_logic[DAYS_BEFORE_NEXT_INSTALMENT_FILTER]) > 30:
        df.insert(
            9,
            DAYS_BEFORE_NEXT_INSTALMENT_FLAG,
            df["DAYS_BEFORE_NEXT_INSTALMENT"].apply(lambda x: eval(modified_days_before_next_instalment_filter)),
        )
    else:
        df.insert(9, DAYS_BEFORE_NEXT_INSTALMENT_FLAG, False)
    df = add_data_to_df(df, include_logic)
    return df


def add_data_to_df(df: pd.DataFrame, include_logic: dict):
    df["INCLUDE_LOGIC"] = json.dumps(include_logic)
    df.insert(0, "CREATED_AT_UTC", pd.to_datetime("now", utc=True))
    return df


def filter_raw_retry_loans_data(df: pd.DataFrame, filters: dict):
    query_parts = []

    for key, value in filters.items():
        if isinstance(value, bool) and value:
            query_parts.append(f"{key}")
        elif key == DAYS_BEFORE_NEXT_INSTALMENT_FILTER and isinstance(value, str) and len(value) > 30:
            query_parts.append(value)

    query_string = " & ".join(query_parts)
    logger.info(f"Final Query String: {query_string}")
    filtered_df = df.query(query_string)
    df = keep_recent_instalment_per_promissory(filtered_df)
    return df


def keep_recent_instalment_per_promissory(df: pd.DataFrame):
    df = df.sort_values(by=["PROMISSORY_ID", "RESPONSE_DT"], ascending=[True, False])
    df["ROW_NUMBER"] = df.groupby("PROMISSORY_ID").cumcount()
    # Filtering to keep only the first row of each group
    df_latest_entries = df[df["ROW_NUMBER"] == 0].drop("ROW_NUMBER", axis=1)
    return df_latest_entries
