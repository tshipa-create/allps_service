from model import service_client, open_asi, instalment
import config
from app_logging import logObject
import xmltodict
from db import save_allps_response_to_snowflake

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
    def authenticate(cls):
        if cls._auth_response_parser is None:
            client = cls.get_client()
            open_asi_auth = open_asi.OpenAsi(
                uid=config.ALLPS_USER,
                pwd=config.ALLPS_PASSWORD,
                machine=config.ALLPS_MACHINE_NAME,
                user_if=config.ALLPS_USER_IF,
                integrator=config.ALLPS_INTEGRATOR,
                product=config.ALLPS_PRODUCT,
                version=config.ALLPS_PRODUCT_VERSION,
            )
            xml_req = open_asi_auth.to_xml()
            method_name = cls.get_method_name(xml_req)
            xml_resp = client.request_data(xml_req, method_name)
            resp_code, resp_msg = open_asi_auth.get_reply_code_and_message(xml_resp)
            save_allps_response_to_snowflake(resp_code, resp_msg, xml_req, xml_resp)
            cls._auth_response_parser = open_asi.OpenAsiResponseParser(xml_resp)
            return cls._auth_response_parser
        return cls._auth_response_parser

    @classmethod
    def get_instalment(cls, promissory_id: str, inst_num: int):
        if cls._auth_response_parser is None:
            cls.authenticate()  # Ensures authentication before proceeding
        open_asi_auth_response_parser = cls._auth_response_parser
        get_instalments = instalment.GetInstalment(
            guid=open_asi_auth_response_parser.guid,
            org_cd=open_asi_auth_response_parser.org,
            branch_cd=open_asi_auth_response_parser.branch,
            promissory_id=promissory_id,
            inst_num=inst_num,
        )
        xml_req = get_instalments.to_xml()
        method_name = cls.get_method_name(xml_req)
        xml_resp = cls.get_client().request_data(xml_req, method_name)
        resp_code, resp_msg = get_instalments.get_reply_code_and_message(xml_resp)
        save_allps_response_to_snowflake(resp_code, resp_msg, xml_req, xml_resp)
        response_parser = instalment.GetInstalmentResponseParser(xml_resp)
        return response_parser

    @classmethod
    def get_method_name(cls, xml_request: str):
        try:
            parsed_xml = xmltodict.parse(xml_request)
            return next(iter(parsed_xml["methods"]))
        except Exception as e:
            logObject.error("Error parsing method name: %s", e)
            return None
