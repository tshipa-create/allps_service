import sys
import os
import unittest
from unittest.mock import patch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from model.open_asi import OpenAsi, OpenAsiResponseParser
from util import normalize_xml

TEST_UID = "test_uid"
TEST_PWD = "test_pwd"
TEST_MACHINE = "test_WINDOWS-PC"
TEST_USER_IF = "test_allps-ws"
TEST_INTEGRATOR = "Test_P42_integrator"
TEST_PRODUCT = "Test_product_P42"
TEST_VERSION = "Test_version_no"

TEST_RESP_GUID = "80E29E1F383840A3A3F4249BCEC4C820"
TEST_RESP_ORG = "0178"
TEST_RESP_BRANCH = "9333"
TEST_RESP_REPLY_CD_SUCCESS = "207"
TEST_RESP_REPLY_STR_SUCCESS = "Request successfully completed (0000)"
TEST_RESP_REPLY_CD_NOT_SUCCESS = "3027"
TEST_RESP_REPLY_STR_NOT_SUCCESS = "Invalid user name or password (3027)"

TEST_OPEN_ASI_REQUEST_XML = f"""
                        <methods>
                            <OpenAsi>
                                <uid>{TEST_UID}</uid>
                                <pwd>{TEST_PWD}</pwd>
                                <machine>{TEST_MACHINE}</machine>
                                <user_if>{TEST_USER_IF}</user_if>
                                <integrator>{TEST_INTEGRATOR}</integrator>
                                <product>{TEST_PRODUCT}</product>
                                <version>{TEST_VERSION}</version>
                            </OpenAsi>
                        </methods>
                        """

TEST_OPEN_ASI_RESPONSE_XML_SUCCESS = f"""
                                <responses>
                                    <OpenAsi>
                                        <guid>{TEST_RESP_GUID}</guid>
                                        <org>{TEST_RESP_ORG}</org>
                                        <branch>{TEST_RESP_BRANCH}</branch>
                                        <reply_cd>{TEST_RESP_REPLY_CD_SUCCESS}</reply_cd>
                                        <reply_str>{TEST_RESP_REPLY_STR_SUCCESS}</reply_str>
                                    </OpenAsi>
                                </responses>
                            """

TEST_OPEN_ASI_RESPONSE_XML_INVALID = "<responses></responses>"

TEST_OPEN_ASI_RESPONSE_XML_ERROR_CODE = f"""
                                <responses>
                                    <OpenAsi>
                                        <guid>{TEST_RESP_GUID}</guid>
                                        <org>{TEST_RESP_ORG}</org>
                                        <branch>{TEST_RESP_BRANCH}</branch>
                                        <reply_cd>{TEST_RESP_REPLY_CD_NOT_SUCCESS}</reply_cd>
                                        <reply_str>{TEST_RESP_REPLY_STR_NOT_SUCCESS}</reply_str>
                                    </OpenAsi>
                                </responses>
                                """

TEST_OPEN_ASI_RESPONSE_XML_MISSING_VALUES = f"""
                                <responses>
                                    <OpenAsi>
                                        <guid>{TEST_RESP_GUID}</guid>
                                        <org></org>
                                        <branch>{TEST_RESP_BRANCH}</branch>
                                    </OpenAsi>
                                </responses>
                                """


class TestOpenAsi(unittest.TestCase):
    def setUp(self):
        self.open_asi = OpenAsi(
            TEST_UID, TEST_PWD, TEST_MACHINE, TEST_USER_IF, TEST_INTEGRATOR, TEST_PRODUCT, TEST_VERSION
        )

    def test_init(self):
        self.assertEqual(self.open_asi.uid, TEST_UID)
        self.assertEqual(self.open_asi.pwd, TEST_PWD)
        self.assertEqual(self.open_asi.machine, TEST_MACHINE)
        self.assertEqual(self.open_asi.user_if, TEST_USER_IF)
        self.assertEqual(self.open_asi.integrator, TEST_INTEGRATOR)
        self.assertEqual(self.open_asi.product, TEST_PRODUCT)
        self.assertEqual(self.open_asi.version, TEST_VERSION)

    def test_to_xml(self):
        expected_xml = normalize_xml(TEST_OPEN_ASI_REQUEST_XML)
        self.assertEqual(normalize_xml(self.open_asi.to_xml().strip()), expected_xml.strip())

    def test_xml_response_to_dict_successfull(self):
        xml_response = TEST_OPEN_ASI_RESPONSE_XML_SUCCESS
        expected_dict = {
            "responses": {
                "OpenAsi": {
                    "guid": TEST_RESP_GUID,
                    "org": TEST_RESP_ORG,
                    "branch": TEST_RESP_BRANCH,
                    "reply_cd": TEST_RESP_REPLY_CD_SUCCESS,
                    "reply_str": TEST_RESP_REPLY_STR_SUCCESS,
                }
            }
        }
        self.assertDictEqual(self.open_asi.xml_response_to_dict(xml_response), expected_dict)

    def test_xml_response_to_dict_with_invalid_xml(self):
        invalid_xml_response = TEST_OPEN_ASI_RESPONSE_XML_INVALID
        self.assertDictEqual(self.open_asi.xml_response_to_dict(invalid_xml_response), {"responses": None})

    def test_xml_response_to_dict_with_error_code(self):
        xml_response = TEST_OPEN_ASI_RESPONSE_XML_ERROR_CODE
        expected_dict = {
            "responses": {
                "OpenAsi": {
                    "guid": TEST_RESP_GUID,
                    "org": TEST_RESP_ORG,
                    "branch": TEST_RESP_BRANCH,
                    "reply_cd": TEST_RESP_REPLY_CD_NOT_SUCCESS,
                    "reply_str": TEST_RESP_REPLY_STR_NOT_SUCCESS,
                }
            }
        }
        self.assertDictEqual(self.open_asi.xml_response_to_dict(xml_response), expected_dict)


class TestOpenAsiResponseParser(unittest.TestCase):
    def setUp(self):
        self.response_xml = TEST_OPEN_ASI_RESPONSE_XML_SUCCESS
        self.response_parser = OpenAsiResponseParser(self.response_xml)

    def test_init(self):
        self.assertEqual(self.response_parser.response_xml, self.response_xml)

    def test_extract_values_successfull(self):
        self.assertEqual(self.response_parser.branch, TEST_RESP_BRANCH)
        self.assertEqual(self.response_parser.guid, TEST_RESP_GUID)
        self.assertEqual(self.response_parser.org, TEST_RESP_ORG)
        self.assertEqual(self.response_parser.reply_cd, TEST_RESP_REPLY_CD_SUCCESS)
        self.assertEqual(self.response_parser.reply_str, TEST_RESP_REPLY_STR_SUCCESS)

    def test_extract_values_with_missing_info(self):
        xml_response_missing_info = TEST_OPEN_ASI_RESPONSE_XML_MISSING_VALUES
        response_parser_missing_info = OpenAsiResponseParser(xml_response_missing_info)
        self.assertEqual(response_parser_missing_info.guid, TEST_RESP_GUID)
        self.assertEqual(response_parser_missing_info.org, None)
        self.assertEqual(response_parser_missing_info.branch, TEST_RESP_BRANCH)

    @patch("model.open_asi.logObject")
    def test_extract_values_with_exception(self, mock_log):
        self.response_parser.response_dict = None  # This will cause an exception in extract_values
        self.response_parser.extract_values()
        mock_log.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
