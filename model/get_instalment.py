import xmltodict
from app_logging import logObject


class GetInstalment:
    def __init__(self, guid: str, org_cd: str, branch_cd: str, promissory_id: str, inst_num: int):
        if not 1 <= inst_num <= 999:
            logObject.error("inst_num (installment number) must be between 1 and 999")
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
            fields = [
                "inst_dt",
                "reply_cd",
                "reply_str",
                "status",
            ]
            for field in fields:
                setattr(self, field, instalment_info.get(field, None))
        except Exception as e:
            logObject.error("Error extracting values from GetInstalmentResponseParser: %s", e)
