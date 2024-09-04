import json
from pandas import DataFrame
from model.allps_service import AllpsService
import util
from logger_config import logger
from db import (
    fetch_raw_retry_loans_data,
    save_results,
)
import boto3
import config
from raw_data_processing import (
    add_days_flag_to_include_logic_dict,
    calculate_days_before_next_instalment_flag,
    filter_raw_retry_loans_data,
)

EXPECTED_INSTALMENT_STATUS = "INCOMPLETE"


def main():
    client = boto3.client("lambda", region_name="us-east-1")
    allps_service_instance = AllpsService()
    allps_service_instance.authenticate()
    df = fetch_raw_retry_loans_data()
    include_logic = add_days_flag_to_include_logic_dict(
        config.RAW_RETRY_LOANS_FILTERS_JSON
    )
    df: DataFrame = calculate_days_before_next_instalment_flag(df, include_logic)

    df_filtered = filter_raw_retry_loans_data(
        df, config.RAW_RETRY_LOANS_FILTERS_JSON
    ).reset_index(drop=True)

    if util.check_loans_data_fetch(df_filtered) is False:
        allps_service_instance.close_asi()
        return

    logger.info("Starting process of editing instalments...")
    count_edit_instalments = 0

    util.add_split_info_cols(df_filtered)

    df_filtered["OLD_AMT"] = None
    df_filtered["NEW_AMT"] = None

    for index, row in df_filtered.iterrows():
        logger.info("-" * 100)
        logger.info(f"Processing row: {index + 1}")
        promissory_id = row["PROMISSORY_ID"]
        install_num = row["INST_NUM"]
        new_action_dt = row["NEW_ACTION_DATE"]

        logger.info(
            f"Getting instalment for promissory_id: {promissory_id}, inst_num: {install_num}"
        )

        get_inst_resp = allps_service_instance.get_instalment(
            promissory_id=promissory_id, inst_num=install_num
        )

        inst_dt: str | None = get_inst_resp.inst_dt
        status: str | None = get_inst_resp.status
        amount: str | None = get_inst_resp.amount

        if inst_dt is None or status is None or amount is None:
            logger.info(
                f"Skipping editing instalment for promissory_id: {promissory_id}, inst_num: {install_num}, could not get instalment data."
            )
            continue

        amt_pct = row["AMT_PCT"]
        old_amt = int(amount)
        new_amt = int(old_amt * row["AMT_PCT"] / 100)
        df_filtered.at[index, "OLD_AMT"] = old_amt
        df_filtered.at[index, "NEW_AMT"] = new_amt

        is_instalment_info_valid = util.validate_full_instalment_info(
            status,
            EXPECTED_INSTALMENT_STATUS,
            inst_dt,  # pylint: disable=no-member
        )
        if not is_instalment_info_valid:
            logger.info(
                f"Skipping editing instalment for promissory_id: {promissory_id}, inst_num: {install_num}..."
            )
            continue

        if amt_pct == 100:
            logger.info(
                f"Editing instalment for promissory_id: {promissory_id}, inst_num: {install_num} with new_action_dt: {new_action_dt}"
            )

            allps_service_instance.edit_instalment(
                promissory_id=promissory_id,
                inst_num=install_num,
                new_action_dt=new_action_dt,
            )

        else:
            logger.info(
                f"Editing instalment for promissory_id: {promissory_id}, inst_num: {install_num} with new_action_dt: {new_action_dt} and with new_amount: {new_amt} ({amt_pct}%)"
            )

            payload = {
                "promissory_id": promissory_id,
                "inst_num": install_num,
                "amount": new_amt,
                "new_action_dt": new_action_dt,
            }

            logger.info(f"Invoking allps_instalment_api lambda, payload: {payload}")

            client.invoke(
                FunctionName="allps_instalment_api",
                InvocationType="Event",
                Payload=json.dumps(payload),
            )

        count_edit_instalments += 1

    logger.info("Saving raw retry loans data to Snowflake")
    save_results(df, config.SF_RETRY_RAW_LOANS_DATA_TABLE)

    util.installments_statistics_from_processings(
        len(df_filtered), count_edit_instalments
    )
    allps_service_instance.close_asi()


if __name__ == "__main__":
    main()
