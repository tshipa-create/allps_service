import os
import sys
import unittest
from unittest.mock import MagicMock, patch


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from test_open_asi import (
    TEST_OPEN_ASI_REQUEST_XML,
    TEST_OPEN_ASI_RESPONSE_XML_SUCCESS,
    TEST_RESP_GUID,
    TEST_RESP_REPLY_CD_SUCCESS,
    TEST_RESP_REPLY_STR_SUCCESS,
)
from test_get_instalment import (
    TEST_GET_INSTALL_REQUEST_XML,
    TEST_GET_INSTALL_RESP_REPLY_CD_SUCCESS,
    TEST_GET_INSTALL_RESP_REPLY_STR_SUCCESS,
    TEST_GET_INSTALL_RESPONSE_XML_SUCCESS,
    TEST_PROMISSORY_ID,
    TEST_INST_NUM,
)
from util import normalize_xml
from tests.test_base_setup import BaseTest
from test_edit_instalment import (
    TEST_EDIT_INSTALL_ACTION_DT,
    TEST_EDIT_INSTALL_REQUEST_XML,
    TEST_EDIT_INSTALL_RESP_REPLY_CD_SUCCESS,
    TEST_EDIT_INSTALL_RESP_REPLY_STR_SUCCESS,
    TEST_EDIT_INSTALL_RESPONSE_XML_SUCCESS,
)


class TestAllpsService(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from model.allps_service import AllpsService

        cls.AllpsService = AllpsService

    def setUp(self):
        # Mock the service_client.RequestClient class
        self.mock_client = MagicMock()
        self.AllpsService.get_client = MagicMock(return_value=self.mock_client)

    def test_get_client(self):
        # Ensure that get_client returns the same client instance
        client1 = self.AllpsService.get_client()
        client2 = self.AllpsService.get_client()
        self.assertEqual(client1, client2)

    @patch("model.allps_service.save_allps_response_to_snowflake")
    @patch("model.allps_service.get_reply_code_and_message")
    def test_authenticate(self, mock_get_reply_code_and_message, mock_save_allps_response_to_snowflake):

        mock_response_xml = TEST_OPEN_ASI_RESPONSE_XML_SUCCESS
        self.mock_client.request_data.return_value = mock_response_xml
        mock_get_reply_code_and_message.return_value = (TEST_RESP_REPLY_CD_SUCCESS, TEST_RESP_REPLY_STR_SUCCESS)

        response_parser = self.AllpsService.authenticate()

        self.mock_client.request_data.assert_called()
        mock_get_reply_code_and_message.called_once_with(mock_response_xml, "OpenAsi")
        mock_save_allps_response_to_snowflake.assert_called()

        self.assertDictEqual(response_parser.response_dict, self.AllpsService._auth_response_parser.response_dict)

    @patch("model.allps_service.save_allps_response_to_snowflake")
    @patch("model.allps_service.is_auth_guid")
    @patch("model.allps_service.get_reply_code_and_message")
    def test_get_instalment(
        self, mock_get_reply_code_and_message, mock_is_auth_guid, mock_save_allps_response_to_snowflake
    ):

        mock_is_auth_guid.return_value = True

        xml_request = normalize_xml(TEST_GET_INSTALL_REQUEST_XML)
        mock_response_xml = TEST_GET_INSTALL_RESPONSE_XML_SUCCESS
        self.mock_client.request_data.return_value = mock_response_xml
        mock_get_reply_code_and_message.return_value = (
            TEST_GET_INSTALL_RESP_REPLY_CD_SUCCESS,
            TEST_GET_INSTALL_RESP_REPLY_STR_SUCCESS,
        )

        self.AllpsService.get_instalment(TEST_PROMISSORY_ID, TEST_INST_NUM)

        mock_is_auth_guid.assert_called_once_with(TEST_RESP_GUID)
        self.mock_client.request_data.assert_called_once_with(xml_request, "GetInstalment")
        mock_get_reply_code_and_message.assert_called_once_with(mock_response_xml, "GetInstalment")
        mock_save_allps_response_to_snowflake.assert_called()

    @patch("model.allps_service.save_allps_response_to_snowflake")
    @patch("model.allps_service.is_auth_guid")
    @patch("model.allps_service.get_reply_code_and_message")
    def test_edit_instalment(
        self, mock_get_reply_code_and_message, mock_is_auth_guid, mock_save_allps_response_to_snowflake
    ):

        mock_is_auth_guid.return_value = True

        xml_request = normalize_xml(TEST_EDIT_INSTALL_REQUEST_XML)
        mock_response_xml = TEST_EDIT_INSTALL_RESPONSE_XML_SUCCESS
        self.mock_client.request_data.return_value = mock_response_xml
        mock_get_reply_code_and_message.return_value = (
            TEST_EDIT_INSTALL_RESP_REPLY_CD_SUCCESS,
            TEST_EDIT_INSTALL_RESP_REPLY_STR_SUCCESS,
        )

        self.AllpsService.edit_instalment(TEST_PROMISSORY_ID, TEST_INST_NUM, TEST_EDIT_INSTALL_ACTION_DT)

        mock_is_auth_guid.assert_called_once_with(TEST_RESP_GUID)
        self.mock_client.request_data.assert_called_once_with(xml_request, "EditInstalment")
        mock_get_reply_code_and_message.assert_called_once_with(mock_response_xml, "EditInstalment")
        mock_save_allps_response_to_snowflake.assert_called()

    def test_get_method_name(self):
        xml_request = TEST_OPEN_ASI_REQUEST_XML
        method_name = self.AllpsService.get_method_name(xml_request)
        self.assertIsNotNone(method_name)
        self.assertEqual(method_name, "OpenAsi")


if __name__ == "__main__":
    unittest.main()
