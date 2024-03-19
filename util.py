from datetime import datetime, timezone
import xmltodict
from app_logging import logObject


def get_reply_code_and_message(xml_response: str, method_name: str):
    response_dict = xmltodict.parse(xml_response)
    reply_code = response_dict["responses"][method_name]["reply_cd"]
    reply_message = response_dict["responses"][method_name]["reply_str"]
    return reply_code, reply_message


def is_valid_date(new_action_dt: datetime) -> bool:
    try:
        new_action_dt.strftime("%Y%m%d")
        return True
    except ValueError:
        return False


def is_auth_guid(guid: str) -> bool:
    if guid is None:
        logObject.error("Authentication failed. Cannot proceed with get_instalment")
        return False
    return True


def check_instalment_status(current_status: str, check_status: str) -> bool:
    if current_status == check_status:
        logObject.info("Instalment status as expected: %s", check_status)
        return True
    logObject.warning(
        "Instalment status not as expected, current_status: %s, expected_status: %s", current_status, check_status
    )
    return False


def check_instalment_not_in_future(installment_date: str) -> bool:
    current_utc_date = datetime.now(timezone.utc).date()
    installment_as_date = datetime.strptime(installment_date, "%Y%m%d").date()
    if installment_as_date > current_utc_date:
        logObject.warning("Instalment date is in future: %s with current date: %s", installment_date, current_utc_date)
        return False
    return True


def validate_full_instalment_info(current_status: str, check_status: str, installment_date: str) -> bool:
    status_valid = check_instalment_status(current_status, check_status)
    date_valid = check_instalment_not_in_future(installment_date)
    return status_valid and date_valid


def installments_statistics_from_processings(total_installments: int, edited_installments: int):
    if total_installments == 0:
        logObject.warning("RUN STATISTICS: No instalments to edit")
    elif total_installments == edited_installments:
        logObject.warning("RUN STATISTICS: All instalments were edited")
    elif total_installments != edited_installments:
        logObject.warning(
            "RUN STATISTICS: Mismatch between total instalments: %d and edited instalments: %d",
            total_installments,
            edited_installments,
        )


def normalize_xml(xml_str: str):
    return "".join(xml_str.split())


def check_loans_data_fetch(df):
    if df is None:
        logObject.error("Error fetching retry loans data. Exiting process...")
        return False
    elif df.empty:
        logObject.warning("No retry loans data found. Exiting process...")
        return False
    return True
