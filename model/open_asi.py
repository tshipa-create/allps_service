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
        # TODO: remove unnecessary fields
        try:
            open_asi_info = self.response_dict.get("responses", {}).get("OpenAsi", {})
            fields = [
                "add_clt_acc",
                "add_clt_pmt",
                "bank_inscription",
                "branch",
                "branch_desc",
                "can_contract",
                "can_inst",
                "can_wal_link",
                "chg_ct_status",
                "chg_dt_adjust",
                "chg_inst_act_dt",
                "chg_inst_amt",
                "chg_track",
                "coll_fields_type",
                "cr_acc_status",
                "cr_acol",
                "cr_acol_auth",
                "cr_acol_offline",
                "cr_acol_rt",
                "cr_aedo",
                "cr_card_acol",
                "cr_card_eft",
                "cr_card_geft",
                "cr_card_naedo",
                "cr_card_seft",
                "cr_eft",
                "cr_geft",
                "cr_naedo",
                "cr_pre_create",
                "cr_seft",
                "cr_wallet",
                "def_acc_type",
                "def_ct_status",
                "def_frequency",
                "def_ifee_type",
                "def_prom_term",
                "def_track_cd",
                "def_track_days",
                "def_wal_sponsor",
                "guid",
                "integrator",
                "link_wal",
                "machine",
                "org",
                "product",
                "pwd",
                "recall_inst",
                "reply_cd",
                "reply_str",
                "response",
                "responseText",
                "uid",
                "user_if",
                "version",
            ]
            for field in fields:
                setattr(self, field, open_asi_info.get(field, None))
        except Exception as e:
            logObject.error("Error extracting values from OpenAsiResponseParser: %s", e)
