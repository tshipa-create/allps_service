from zeep import Client
from app_logging import logObject


class RequestClient:
    def __init__(self, wsdl_url: str):
        self.client = Client(wsdl=wsdl_url)

    def request_data(self, xml_request: str, method_name: str):
        try:
            request_data = {"xmlrequest": xml_request}
            logObject.warning("Requesting data from ALLPS: %s", method_name)
            return self.client.service.Call(**request_data)
        except Exception as e:
            logObject.error("Error requesting data from ALLPS: %s", e)
            return None
