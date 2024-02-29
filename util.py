from datetime import datetime
import xmltodict
from app_logging import logObject


def get_reply_code_and_message(xml_response: str, method_name: str):
    response_dict = xmltodict.parse(xml_response)
    reply_code = response_dict["responses"][method_name]["reply_cd"]
    reply_message = response_dict["responses"][method_name]["reply_str"]
    return reply_code, reply_message


def is_valid_date(new_action_dt: str):
    try:
        datetime.strptime(new_action_dt, "%Y%m%d")
        return True
    except ValueError:
        return False


def is_auth_guid(guid: str):
    if guid is None:
        logObject.error("Authentication failed. Cannot proceed with get_instalment")
        return False
    return True


def check_instalment_status(current_status: str, check_status: str):
    if current_status == check_status:
        logObject.info("Instalment status as expected: %s", check_status)
        return True
    logObject.error(
        "Instalment status not as expected, current_status: %s, expected_status: %s", current_status, check_status
    )
    return False
