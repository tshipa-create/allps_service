from model.allps_service import AllpsService
import util
from logger_config import logger
from db import fetch_raw_retry_loans_data, fetch_daily_monitoring_data, general_save_to_snowflake
import config
from slack_integration import slack_post_msg
from raw_data_processing import (
    add_days_flag_to_include_logic_dict,
    calculate_days_before_next_instalment_flag,
    filter_raw_retry_loans_data,
)

EXPECTED_INSTALMENT_STATUS = "INCOMPLETE"


def main():
    allps_service_instance = AllpsService()
    allps_service_instance.authenticate()
    df = fetch_raw_retry_loans_data()
    include_logic = add_days_flag_to_include_logic_dict(config.RAW_RETRY_LOANDS_FILTERS_JSON)
    df = calculate_days_before_next_instalment_flag(df, include_logic)
    logger.info("Saving raw retry loans data to Snowflake")
    general_save_to_snowflake(df, config.SF_RETRY_RAW_LOANS_DATA_TABLE)
    df_filtered = filter_raw_retry_loans_data(df, config.RAW_RETRY_LOANDS_FILTERS_JSON).reset_index(drop=True)
    if util.check_loans_data_fetch(df_filtered) is False:
        allps_service_instance.close_asi()
        return
    logger.info("Starting process of editing instalments...")
    count_edit_instalments = 0
    for index, row in df_filtered.iterrows():
        logger.info("-" * 100)
        logger.info(f"Processing row: {index + 1}")
        promissory_id = row["PROMISSORY_ID"]
        install_num = row["INST_NUM"]
        new_action_dt = row["NEW_ACTION_DATE"]
        logger.info(f"Getting instalment for promissory_id: {promissory_id}, inst_num: {install_num}")
        get_instalment_response_parser = allps_service_instance.get_instalment(
            promissory_id=promissory_id, inst_num=install_num
        )
        is_instalment_info_valid = util.validate_full_instalment_info(
            get_instalment_response_parser.status,
            EXPECTED_INSTALMENT_STATUS,
            get_instalment_response_parser.inst_dt,  # pylint: disable=no-member
        )
        if not is_instalment_info_valid:
            logger.info(f"Skipping editing instalment for promissory_id: {promissory_id}, inst_num: {install_num}...")
            continue
        logger.info(
            f"Editing instalment for promissory_id: {promissory_id}, inst_num: {install_num} with new_action_dt: {new_action_dt}"
        )
        allps_service_instance.edit_instalment(
            promissory_id=promissory_id, inst_num=install_num, new_action_dt=new_action_dt
        )
        count_edit_instalments += 1
    util.installments_statistics_from_processings(len(df), count_edit_instalments)
    allps_service_instance.close_asi()
    if config.ENABLE_SLACK_NOTIFICATIONS:
        df_monitoring = fetch_daily_monitoring_data()
        slack_post_msg(df_monitoring)


if __name__ == "__main__":
    main()
