from datetime import datetime, timedelta
from model import service_client, open_asi, edit_instalment, get_instalment
import config
from db import save_allps_response_to_snowflake
from util import normalize_xml, get_reply_code_and_message, is_auth_guid
import xmltodict
from logger_config import logger


ALLPS_WSDL_URL = f"{config.ALLPS_HOST}?wsdl"


class AllpsService:
    # class variables, not an instance variable
    _client = None
    _auth_response_parser = None

    @classmethod  # classmethod So those would stay the same for all instances of the class
    def get_client(cls):
        if cls._client is None:
            cls._client = service_client.RequestClient(wsdl_url=f"{config.ALLPS_HOST}?wsdl")
        return cls._client

    @classmethod
    def submit_req_and_log_response(cls, xml_req):
        method_name = cls.get_method_name(xml_req)
        xml_resp = cls.get_client().request_data(xml_req, method_name)
        resp_code, resp_msg = get_reply_code_and_message(xml_resp, method_name)
        logger.warning(f'ALLPS {method_name} response_code: "{resp_code}", response_message: "{resp_msg}"')
        save_allps_response_to_snowflake(resp_code, resp_msg, method_name, xml_req, xml_resp)
        return xml_resp, resp_code

    @classmethod
    def authenticate(cls):
        if cls._auth_response_parser is None:
            open_asi_auth = open_asi.OpenAsi(
                uid=config.ALLPS_USER,
                pwd=config.ALLPS_PASSWORD,
                machine=config.ALLPS_MACHINE_NAME,
                user_if=config.ALLPS_USER_IF,
                integrator=config.ALLPS_INTEGRATOR,
                product=config.ALLPS_PRODUCT,
                version=config.ALLPS_PRODUCT_VERSION,
            )
            xml_req = normalize_xml(open_asi_auth.to_xml())
            xml_resp, _ = cls.submit_req_and_log_response(xml_req)
            cls._auth_response_parser = open_asi.OpenAsiResponseParser(xml_resp)
            return cls._auth_response_parser
        return cls._auth_response_parser

    @classmethod
    def get_instalment(cls, promissory_id: str, inst_num: int):
        if cls._auth_response_parser is None:
            cls.authenticate()  # Ensures authentication before proceeding
        open_asi_auth_response_parser = cls._auth_response_parser
        if is_auth_guid(open_asi_auth_response_parser.guid) is False:
            raise Exception("GUID is false, exiting")
        get_install = get_instalment.GetInstalment(
            guid=open_asi_auth_response_parser.guid,
            org_cd=open_asi_auth_response_parser.org,
            branch_cd=open_asi_auth_response_parser.branch,
            promissory_id=promissory_id,
            inst_num=inst_num,
        )
        xml_req = normalize_xml(get_install.to_xml())
        xml_resp, _ = cls.submit_req_and_log_response(xml_req)
        response_parser = get_instalment.GetInstalmentResponseParser(xml_resp)
        return response_parser

    @classmethod
    def edit_instalment(cls, promissory_id: str, inst_num: int, new_action_dt: datetime.date):
        if cls._auth_response_parser is None:
            cls.authenticate()
        open_asi_auth_response_parser = cls._auth_response_parser
        if is_auth_guid(open_asi_auth_response_parser.guid) is False:
            exit(1)
        edit_install = edit_instalment.EditInstalment(
            guid=open_asi_auth_response_parser.guid,
            org_cd=open_asi_auth_response_parser.org,
            branch_cd=open_asi_auth_response_parser.branch,
            promissory_id=promissory_id,
            inst_num=inst_num,
            new_action_dt=new_action_dt,
        )
        xml_req = normalize_xml(edit_install.to_xml())
        xml_resp, resp_code = cls.submit_req_and_log_response(xml_req)
        retry_count = 0
        while resp_code in config.ALLPS_RESPONSE_CODES_RETRY_LIST:
            retry_count += 1
            new_action_dt = new_action_dt + timedelta(days=1)
            logger.warning(
                f'Retry #{retry_count}: Retrying edit_instalment because of response_code: "{resp_code}" for promissory_id: "{promissory_id}", inst_num: "{inst_num}" and with new_action_dt: "{new_action_dt}"'
            )
            edit_install = edit_instalment.EditInstalment(
                guid=open_asi_auth_response_parser.guid,
                org_cd=open_asi_auth_response_parser.org,
                branch_cd=open_asi_auth_response_parser.branch,
                promissory_id=promissory_id,
                inst_num=inst_num,
                new_action_dt=new_action_dt,
            )
            xml_req = normalize_xml(edit_install.to_xml())
            xml_resp, resp_code = cls.submit_req_and_log_response(xml_req)
        response_parser = edit_instalment.EditInstalmentResponseParser(xml_resp)
        return response_parser

    @classmethod
    def close_asi(cls):
        close_asi = open_asi.CloseAsi(guid=cls._auth_response_parser.guid)
        xml_req = normalize_xml(close_asi.to_xml())
        cls.submit_req_and_log_response(xml_req)

    @classmethod
    def get_method_name(cls, xml_request: str):
        try:
            parsed_xml = xmltodict.parse(xml_request)
            return next(iter(parsed_xml["methods"]))
        except Exception as e:
            logger.error(f"Error parsing method name: {e}")
            return None
