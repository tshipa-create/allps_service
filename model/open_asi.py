import xmltodict


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
    