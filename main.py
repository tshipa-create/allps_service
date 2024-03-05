from model.allps_service import AllpsService
import util
import pandas as pd
from app_logging import logObject

EXPECTED_INSTALMENT_STATUS = "INCOMPLETE"

# TODO: Add Slack notification as this is important process for business?


def main():
    allps_service_instance = AllpsService()
    allps_service_instance.authenticate()
    # TODO: replace with actual data. With from db.fetch_retry_loans_data()
    df = pd.DataFrame(
        {"PROMISSORY_ID": ["00004C40F2", "00004C40F2"], "INST_NUM": [1, 21], "NEW_ACTION_DT": ["2024032", "20240313"]}
    )
    logObject.warning("Starting process of editing instalments...")
    count_edit_instalments = 0
    for index, row in df.iterrows():
        logObject.warning("-" * 100)
        logObject.warning("Processing row: %s", index + 1)
        promissory_id = row["PROMISSORY_ID"]
        install_num = row["INST_NUM"]
        new_action_dt = row["NEW_ACTION_DT"]
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
