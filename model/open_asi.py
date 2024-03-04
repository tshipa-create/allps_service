import xmltodict
from app_logging import logObject


class OpenAsi:
    def __init__(self, uid: str, pwd: str, machine: str, user_if: str, integrator: str, product: str, version: str):
        self.uid = uid
        self.pwd = pwd
        self.machine = machine
        self.user_if = user_if
        self.integrator = integrator
        self.product = product
        self.version = version

    def to_xml(self):
        return f"""
        <methods>
            <OpenAsi>
                <uid>{self.uid}</uid>
                <pwd>{self.pwd}</pwd>
                <machine>{self.machine}</machine>
                <user_if>{self.user_if}</user_if>
                <integrator>{self.integrator}</integrator>
                <product>{self.product}</product>
                <version>{self.version}</version>
            </OpenAsi>
        </methods>
        """

    def xml_response_to_dict(self, xml_response: str):
        return xmltodict.parse(xml_response)


class OpenAsiResponseParser:
    def __init__(self, response_xml: str):
        self.response_xml = response_xml
        self.response_dict = xmltodict.parse(response_xml)
        self.extract_values()

    def extract_values(self):
        try:
            open_asi_info = self.response_dict.get("responses", {}).get("OpenAsi", {})
            self.branch = open_asi_info.get("branch", None)
            self.guid = open_asi_info.get("guid", None)
            self.org = open_asi_info.get("org", None)
            self.reply_cd = open_asi_info.get("reply_cd", None)
            self.reply_str = open_asi_info.get("reply_str", None)
        except Exception as e:
            logObject.error("Error extracting values from OpenAsiResponseParser: %s", e)
