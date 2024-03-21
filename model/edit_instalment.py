from datetime import datetime
import util
import xmltodict
from app_logging import logObject
import config


class EditInstalment:
    def __init__(
        self, guid: str, org_cd: str, branch_cd: str, promissory_id: str, inst_num: int, new_action_dt: datetime.date
    ):
        if not 1 <= inst_num <= 999:
            logObject.error("inst_num (installment number) must be between 1 and 999")
        self.guid = guid
        self.org_cd = org_cd
        self.branch_cd = branch_cd
        self.promissory_id = promissory_id
        self.inst_num = inst_num
        self.new_action_dt = util.format_date_to_string(new_action_dt)  # format date to string for xml 'YYYYMMDD'

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
                <new_track_cd>{config.ALLPS_NEW_TRACK_CODE}</new_track_cd>
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

            self.inst_num = edit_instalment_info.get("inst_num", None)
            self.new_action_dt = edit_instalment_info.get("new_action_dt", None)
            self.reply_cd = edit_instalment_info.get("reply_cd", None)
            self.reply_str = edit_instalment_info.get("reply_str", None)
        except Exception as e:
            logObject.error("Error extracting values from EditInstalmentResponseParser: %s", e)
