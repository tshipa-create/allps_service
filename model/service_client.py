from zeep import Client
from logger_config import logger


class RequestClient:
    def __init__(self, wsdl_url: str):
        self.client = Client(wsdl=wsdl_url)

    def request_data(self, xml_request: str, method_name: str):
        try:
            request_data = {"xmlrequest": xml_request}
            if method_name == "OpenAsi":
                logger.info(f"Requesting data from ALLPS: {method_name} with Host: '{self.client.wsdl.location}'")
            else:
                logger.info(f"Requesting data from ALLPS: {method_name}")
            return self.client.service.Call(**request_data)
        except Exception as e:
            logger.exception(f"Error requesting data from ALLPS: {e}")
            return None
