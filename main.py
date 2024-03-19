from model.allps_service import AllpsService
import util
from app_logging import logObject
from db import fetch_retry_loans_data


EXPECTED_INSTALMENT_STATUS = "INCOMPLETE"


def main():
    allps_service_instance = AllpsService()
    allps_service_instance.authenticate()
    df = fetch_retry_loans_data()
    if util.check_loans_data_fetch(df) is False:
        allps_service_instance.close_asi()
        return
    logObject.warning("Starting process of editing instalments...")
    count_edit_instalments = 0
    for index, row in df.iterrows():
        logObject.warning("-" * 100)
        logObject.warning("Processing row: %s", index + 1)
        promissory_id = row["PROMISSORY_ID"]
        install_num = row["INST_NUM"]
        new_action_dt = row["NEW_ACTION_DATE"]
        logObject.warning("Getting instalment for promissory_id: %s, inst_num: %s", promissory_id, install_num)
        get_instalment_response_parser = allps_service_instance.get_instalment(
            promissory_id=promissory_id, inst_num=install_num
        )
        is_instalment_info_valid = util.validate_full_instalment_info(
            get_instalment_response_parser.status,
            EXPECTED_INSTALMENT_STATUS,
            get_instalment_response_parser.inst_dt,  # pylint: disable=no-member
        )
        if not is_instalment_info_valid:
            logObject.warning(
                "Skipping editing instalment for promissory_id: %s, inst_num: %s...", promissory_id, install_num
            )
            continue
        logObject.warning("Editing instalment for promissory_id: %s, inst_num: %s...", promissory_id, install_num)
        allps_service_instance.edit_instalment(
            promissory_id=promissory_id, inst_num=install_num, new_action_dt=new_action_dt
        )
        count_edit_instalments += 1
    util.installments_statistics_from_processings(len(df), count_edit_instalments)
    allps_service_instance.close_asi()


if __name__ == "__main__":
    main()
