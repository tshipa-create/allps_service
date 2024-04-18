from model.allps_service import AllpsService
import util
from logger_config import logger
from db import fetch_retry_loans_data, fetch_daily_monitoring_data
import config
from slack_integration import slack_post_msg

EXPECTED_INSTALMENT_STATUS = "INCOMPLETE"


def main():
    allps_service_instance = AllpsService()
    allps_service_instance.authenticate()
    df = fetch_retry_loans_data()
    if util.check_loans_data_fetch(df) is False:
        allps_service_instance.close_asi()
        return
    logger.warning("Starting process of editing instalments...")
    count_edit_instalments = 0
    for index, row in df.iterrows():
        logger.warning("-" * 100)
        logger.warning(f"Processing row: {index + 1}")
        promissory_id = "00004C8D80"  # row["PROMISSORY_ID"]
        install_num = 20  # row["INST_NUM"]
        from datetime import timedelta

        new_action_dt = row["NEW_ACTION_DATE"] - timedelta(days=2)
        logger.warning(f"Getting instalment for promissory_id: {promissory_id}, inst_num: {install_num}")
        get_instalment_response_parser = allps_service_instance.get_instalment(
            promissory_id=promissory_id, inst_num=install_num
        )
        is_instalment_info_valid = util.validate_full_instalment_info(
            get_instalment_response_parser.status,
            EXPECTED_INSTALMENT_STATUS,
            get_instalment_response_parser.inst_dt,  # pylint: disable=no-member
        )
        if not is_instalment_info_valid:
            logger.warning(
                f"Skipping editing instalment for promissory_id: {promissory_id}, inst_num: {install_num}..."
            )
            continue
        logger.warning(
            f"Editing instalment for promissory_id: {promissory_id}, inst_num: {install_num} with new_action_dt: {new_action_dt}"
        )
        allps_service_instance.edit_instalment(
            promissory_id=promissory_id, inst_num=install_num, new_action_dt=new_action_dt
        )
        count_edit_instalments += 1
        exit(1)
    util.installments_statistics_from_processings(len(df), count_edit_instalments)
    allps_service_instance.close_asi()
    if config.ENABLE_SLACK_NOTIFICATIONS:
        df_monitoring = fetch_daily_monitoring_data()
        slack_post_msg(df_monitoring)


if __name__ == "__main__":
    main()
