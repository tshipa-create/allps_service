import xmltodict
from logger_config import logger


class GetInstalment:
    def __init__(self, guid: str, org_cd: str, branch_cd: str, promissory_id: str, inst_num: int):
        if not 1 <= inst_num <= 999:
            logger.exception("inst_num (installment number) must be between 1 and 999")
        self.guid = guid
        self.org_cd = org_cd
        self.branch_cd = branch_cd
        self.promissory_id = promissory_id
        self.inst_num = inst_num

    def to_xml(self):
        return f"""
        <methods>
            <GetInstalment>
                <guid>{self.guid}</guid>
                <org_cd>{self.org_cd}</org_cd>
                <branch_cd>{self.branch_cd}</branch_cd>
                <promissory_id>{self.promissory_id}</promissory_id>
                <inst_num>{self.inst_num}</inst_num>
            </GetInstalment>
        </methods>
        """

    def xml_response_to_dict(self, xml_response: str):
        return xmltodict.parse(xml_response)


class GetInstalmentResponseParser:
    def __init__(self, response_xml: str):
        self.response_xml = response_xml
        self.response_dict = xmltodict.parse(response_xml)
        self.status = None
        self.extract_values()

    def extract_values(self):
        try:
            instalment_info = self.response_dict.get("responses", {}).get("GetInstalment", {})
            self.inst_dt = instalment_info.get("inst_dt", None)
            self.status = instalment_info.get("status", None)
            self.reply_cd = instalment_info.get("reply_cd", None)
            self.reply_str = instalment_info.get("reply_str", None)
        except Exception as e:
            logger.exception(f"Error extracting values from GetInstalmentResponseParser: {e}")
