from zeep import Client


class RequestClient:
    def __init__(self, wsdl_url):
        self.client = Client(wsdl=wsdl_url)

    def request_data(self, xml_request: str):
        request_data = {"xmlrequest": xml_request}
        return self.client.service.Call(**request_data)
