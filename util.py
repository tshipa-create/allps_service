from datetime import datetime, timezone
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
    logger.info(f"Instalment status not as expected, current_status: {current_status}, check_status: {check_status}")
    return False


def check_instalment_not_in_future(installment_date: str) -> bool:
    current_utc_date = datetime.now(timezone.utc).date()
    installment_as_date = datetime.strptime(installment_date, "%Y%m%d").date()
    if installment_as_date > current_utc_date:
        logger.info(f"Instalment date is in future: {installment_date} with current date: {current_utc_date}")
        return False
    return True


def validate_full_instalment_info(current_status: str, check_status: str, installment_date: str) -> bool:
    status_valid = check_instalment_status(current_status, check_status)
    date_valid = check_instalment_not_in_future(installment_date)
    return status_valid and date_valid


def installments_statistics_from_processings(total_installments: int, edited_installments: int):
    if total_installments == 0:
        logger.warning("RUN STATISTICS: No instalments to edit")
    elif total_installments == edited_installments:
        logger.info("RUN STATISTICS: All instalments were edited")
    elif total_installments != edited_installments:
        logger.warning(
            f"RUN STATISTICS: Mismatch between total instalments: {total_installments} and edited instalments: {edited_installments}"
        )


def normalize_xml(xml_str: str):
    return "".join(xml_str.split())


def check_loans_data_fetch(df):
    if df is None:
        logger.exception("Error fetching retry loans data. Exiting process...")
        return False
    elif df.empty:
        logger.info("No retry loans data found. Exiting process...")
        return False
    return True
