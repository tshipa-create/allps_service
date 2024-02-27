import xmltodict


class GetInstalment:
    def __init__(self, guid: str, org_cd: str, branch_cd: str, promissory_id: str, inst_num: int):
        if not 1 <= inst_num <= 999:
            raise ValueError("inst_num (installment number) must be between 1 and 999")
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

    def get_reply_code_and_message(self, xml_response: str):
        response_dict = self.xml_response_to_dict(xml_response)
        reply_code = response_dict["responses"]["GetInstalment"]["reply_cd"]
        reply_message = response_dict["responses"]["GetInstalment"]["reply_str"]
        return reply_code, reply_message
