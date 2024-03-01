import util
import xmltodict
from app_logging import logObject


class EditInstalment:
    def __init__(self, guid: str, org_cd: str, branch_cd: str, promissory_id: str, inst_num: int, new_action_dt: str):
        if not 1 <= inst_num <= 999:
            logObject.error("inst_num (installment number) must be between 1 and 999")
        if util.is_valid_date(new_action_dt) is False:
            logObject.error("new_action_dt (new action date) must be in the format YYYYMMDD")
        self.guid = guid
        self.org_cd = org_cd
        self.branch_cd = branch_cd
        self.promissory_id = promissory_id
        self.inst_num = inst_num
        self.new_action_dt = new_action_dt

    def to_xml(self):
        return f"""
        <methods>
            <EditInstalment>
                <guid>{self.guid}</guid>
                <org_cd>{self.org_cd}</org_cd>
                <branch_cd>{self.branch_cd}</branch_cd>
                <promissory_id>{self.promissory_id}</promissory_id>
                <inst_num>{self.inst_num}</inst_num>
                <new_action_dt>{self.new_action_dt}</new_action_dt>
            </EditInstalment>
        </methods>
        """

    def xml_response_to_dict(self, xml_response: str):
        return xmltodict.parse(xml_response)


class EditInstalmentResponseParser:
    def __init__(self, response_xml: str):
        self.response_xml = response_xml
        self.response_dict = xmltodict.parse(response_xml)
        self.status = None
        self.extract_values()

    def extract_values(self):
        try:
            edit_instalment_info = self.response_dict.get("responses", {}).get("EditInstalment", {})
            fields = [
                "inst_num",
                "new_action_dt",
                "reply_cd",
                "reply_str",
            ]
            for field in fields:
                setattr(self, field, edit_instalment_info.get(field, None))
        except Exception as e:
            logObject.error("Error extracting values from EditInstalmentResponseParser: %s", e)
