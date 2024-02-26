from zeep import Client
import model.open_asi as open_asi
from icecream import ic
import config

ALLPS_WSDL_URL = f"{config.ALLPS_HOST}?wsdl"

if __name__ == "__main__":
    client = Client(wsdl=ALLPS_WSDL_URL)
    open_asi = open_asi.OpenAsi(
        uid=config.ALLPS_USER,
        pwd=config.ALLPS_PASSWORD,
        machine=config.ALLPS_MACHINE_NAME,
        user_if=config.ALLPS_USER_IF,
        integrator=config.ALLPS_INTEGRATOR,
        product=config.ALLPS_PRODUCT,
        version=config.ALLPS_PRODUCT_VERSION,
    )
    request_data = {"xmlrequest": open_asi.to_xml()}
    open_asi_response = client.service.Call(**request_data)
    ic(open_asi.to_xml())
    ic(open_asi.xml_response_to_dict(open_asi_response))
