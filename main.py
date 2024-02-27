from model import installment, service_client
from model import open_asi
from icecream import ic
import config

ALLPS_WSDL_URL = f"{config.ALLPS_HOST}?wsdl"


if __name__ == "__main__":
    open_asi_auth = open_asi.OpenAsi(
        uid=config.ALLPS_USER,
        pwd=config.ALLPS_PASSWORD,
        machine=config.ALLPS_MACHINE_NAME,
        user_if=config.ALLPS_USER_IF,
        integrator=config.ALLPS_INTEGRATOR,
        product=config.ALLPS_PRODUCT,
        version=config.ALLPS_PRODUCT_VERSION,
    )
    client = service_client.RequestClient(wsdl_url=ALLPS_WSDL_URL)
    open_asi_auth_xml_resp = client.request_data(open_asi_auth.to_xml())
    open_asi_auth_response_dict = open_asi_auth.xml_response_to_dict(open_asi_auth_xml_resp)
    open_asi_auth_response_parser = open_asi.OpenAsiResponseParser(open_asi_auth_xml_resp)
    ic(open_asi_auth_response_dict)
    promissory_id = "00004CDB46"
    # TODO: promissory_id and inst_num are needed to get instalments
    get_instalments = installment.GetInstalment(
        guid=open_asi_auth_response_parser.guid,
        org_cd=open_asi_auth_response_parser.org,
        branch_cd=open_asi_auth_response_parser.branch,
        promissory_id=promissory_id,
        inst_num=1,
    )
    print(get_instalments.to_xml())
    get_instalments_xml_resp = client.request_data(get_instalments.to_xml())
    ic(get_instalments.xml_response_to_dict(get_instalments_xml_resp))
