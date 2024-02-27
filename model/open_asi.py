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


class OpenAsiResponseParser:
    def __init__(self, response_xml: dict):
        # TODO: do we need to add headers as well?
        self.request_xml = None
        self.response_xml = response_xml
        self.response_dict = xmltodict.parse(response_xml)
        self.add_clt_acc = self.response_dict["responses"]["OpenAsi"]["add_clt_acc"]
        self.add_clt_pmt = self.response_dict["responses"]["OpenAsi"]["add_clt_pmt"]
        self.bank_inscription = self.response_dict["responses"]["OpenAsi"]["bank_inscription"]
        self.branch = self.response_dict["responses"]["OpenAsi"]["branch"]
        self.branch_desc = self.response_dict["responses"]["OpenAsi"]["branch_desc"]
        self.can_contract = self.response_dict["responses"]["OpenAsi"]["can_contract"]
        self.can_inst = self.response_dict["responses"]["OpenAsi"]["can_inst"]
        self.can_wal_link = self.response_dict["responses"]["OpenAsi"]["can_wal_link"]
        self.chg_ct_status = self.response_dict["responses"]["OpenAsi"]["chg_ct_status"]
        self.chg_dt_adjust = self.response_dict["responses"]["OpenAsi"]["chg_dt_adjust"]
        self.chg_inst_act_dt = self.response_dict["responses"]["OpenAsi"]["chg_inst_act_dt"]
        self.chg_inst_amt = self.response_dict["responses"]["OpenAsi"]["chg_inst_amt"]
        self.chg_track = self.response_dict["responses"]["OpenAsi"]["chg_track"]
        self.coll_fields_type = self.response_dict["responses"]["OpenAsi"]["coll_fields_type"]
        self.cr_acc_status = self.response_dict["responses"]["OpenAsi"]["cr_acc_status"]
        self.cr_acol = self.response_dict["responses"]["OpenAsi"]["cr_acol"]
        self.cr_acol_auth = self.response_dict["responses"]["OpenAsi"]["cr_acol_auth"]
        self.cr_acol_offline = self.response_dict["responses"]["OpenAsi"]["cr_acol_offline"]
        self.cr_acol_rt = self.response_dict["responses"]["OpenAsi"]["cr_acol_rt"]
        self.cr_aedo = self.response_dict["responses"]["OpenAsi"]["cr_aedo"]
        self.cr_card_acol = self.response_dict["responses"]["OpenAsi"]["cr_card_acol"]
        self.cr_card_eft = self.response_dict["responses"]["OpenAsi"]["cr_card_eft"]
        self.cr_card_geft = self.response_dict["responses"]["OpenAsi"]["cr_card_geft"]
        self.cr_card_naedo = self.response_dict["responses"]["OpenAsi"]["cr_card_naedo"]
        self.cr_card_seft = self.response_dict["responses"]["OpenAsi"]["cr_card_seft"]
        self.cr_eft = self.response_dict["responses"]["OpenAsi"]["cr_eft"]
        self.cr_geft = self.response_dict["responses"]["OpenAsi"]["cr_geft"]
        self.cr_naedo = self.response_dict["responses"]["OpenAsi"]["cr_naedo"]
        self.cr_pre_create = self.response_dict["responses"]["OpenAsi"]["cr_pre_create"]
        self.cr_seft = self.response_dict["responses"]["OpenAsi"]["cr_seft"]
        self.cr_wallet = self.response_dict["responses"]["OpenAsi"]["cr_wallet"]
        self.def_acc_type = self.response_dict["responses"]["OpenAsi"]["def_acc_type"]
        self.def_ct_status = self.response_dict["responses"]["OpenAsi"]["def_ct_status"]
        self.def_frequency = self.response_dict["responses"]["OpenAsi"]["def_frequency"]
        self.def_ifee_type = self.response_dict["responses"]["OpenAsi"]["def_ifee_type"]
        self.def_prom_term = self.response_dict["responses"]["OpenAsi"]["def_prom_term"]
        self.def_track_cd = self.response_dict["responses"]["OpenAsi"]["def_track_cd"]
        self.def_track_days = self.response_dict["responses"]["OpenAsi"]["def_track_days"]
        self.def_wal_sponsor = self.response_dict["responses"]["OpenAsi"]["def_wal_sponsor"]
        self.guid = self.response_dict["responses"]["OpenAsi"]["guid"]
        self.integrator = self.response_dict["responses"]["OpenAsi"]["integrator"]
        self.link_wal = self.response_dict["responses"]["OpenAsi"]["link_wal"]
        self.machine = self.response_dict["responses"]["OpenAsi"]["machine"]
        self.org = self.response_dict["responses"]["OpenAsi"]["org"]
        self.product = self.response_dict["responses"]["OpenAsi"]["product"]
        self.pwd = self.response_dict["responses"]["OpenAsi"]["pwd"]
        self.recall_inst = self.response_dict["responses"]["OpenAsi"]["recall_inst"]
        self.reply_cd = self.response_dict["responses"]["OpenAsi"]["reply_cd"]
        self.reply_str = self.response_dict["responses"]["OpenAsi"]["reply_str"]
        self.response = self.response_dict["responses"]["OpenAsi"]["response"]
        self.responseText = self.response_dict["responses"]["OpenAsi"]["responseText"]
        self.uid = self.response_dict["responses"]["OpenAsi"]["uid"]
        self.user_if = self.response_dict["responses"]["OpenAsi"]["user_if"]
        self.version = self.response_dict["responses"]["OpenAsi"]["version"]
