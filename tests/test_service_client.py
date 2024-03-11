import sys
import os
import unittest
from unittest.mock import Mock

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from model.service_client import RequestClient
from model.allps_service import ALLPS_WSDL_URL
from test_open_asi import (
    TEST_OPEN_ASI_REQUEST_XML,
    TEST_OPEN_ASI_RESPONSE_XML_SUCCESS,
)
from test_get_instalment import (
    TEST_GET_INSTALL_REQUEST_XML,
    TEST_GET_INSTALL_RESPONSE_XML_SUCCESS,
)
from test_edit_instalment import TEST_EDIT_INSTALL_REQUEST_XML, TEST_EDIT_INSTALL_RESPONSE_XML_SUCCESS
from util import normalize_xml


class TestServiceClient(unittest.TestCase):
    def setUp(self):
        self.wsdl_url = ALLPS_WSDL_URL
        self.client = RequestClient(self.wsdl_url)

    def test_request_open_asi_data_success(self):
        method_name = "OpenAsi"
        xml_request = normalize_xml(TEST_OPEN_ASI_REQUEST_XML)
        xml_response = TEST_OPEN_ASI_RESPONSE_XML_SUCCESS
        self.client.client.service.Call = Mock(return_value=xml_response)
        result = self.client.request_data(xml_request, method_name)
        self.assertEqual(result, xml_response)
        self.client.client.service.Call.assert_called_once_with(xmlrequest=xml_request)

    def test_request_open_asi_data_exception(self):
        # Mock the client.service.Call method to raise an exception
        self.client.client.service.Call = Mock(side_effect=Exception("Some error"))
        method_name = "OpenAsi"
        xml_request = normalize_xml(TEST_OPEN_ASI_REQUEST_XML)
        result = self.client.request_data(xml_request, method_name)
        self.assertIsNone(result)
        self.client.client.service.Call.assert_called_once_with(xmlrequest=xml_request)

    def test_request_data_GetInstalment(self):
        xml_request = normalize_xml(TEST_GET_INSTALL_REQUEST_XML)
        method_name = "GetInstalment"
        xml_response = TEST_GET_INSTALL_RESPONSE_XML_SUCCESS
        self.client.client.service.Call = Mock(return_value=xml_response)
        result = self.client.request_data(xml_request, method_name)

        self.assertEqual(result, xml_response)
        self.client.client.service.Call.assert_called_once_with(xmlrequest=xml_request)

    # TODO: change to editInstalment when the method is implemented
    def test_request_data_EditInstalment(self):
        xml_request = normalize_xml(TEST_EDIT_INSTALL_REQUEST_XML)
        method_name = "EditInstalment"
        xml_response = TEST_EDIT_INSTALL_RESPONSE_XML_SUCCESS
        self.client.client.service.Call = Mock(return_value=xml_response)
        result = self.client.request_data(xml_request, method_name)

        self.assertEqual(result, xml_response)
        self.client.client.service.Call.assert_called_once_with(xmlrequest=xml_request)


if __name__ == "__main__":
    unittest.main()
