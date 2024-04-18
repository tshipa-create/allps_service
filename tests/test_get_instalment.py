import os
import sys
import unittest
from unittest.mock import patch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from tests.test_base_setup import BaseTest
from test_open_asi import TEST_RESP_GUID, TEST_RESP_ORG, TEST_RESP_BRANCH
from util import normalize_xml

EXPECTED_INSTALMENT_STATUS = "INCOMPLETE"
TEST_PROMISSORY_ID = "TEST_00004C40F2"
TEST_INST_DT = "20240101"
TEST_INST_NUM = 99
TEST_GET_INSTALL_RESP_REPLY_CD_SUCCESS = "207"
TEST_GET_INSTALL_RESP_REPLY_STR_SUCCESS = "Request successfully completed (0000)"
TEST_GET_INSTALL_RESP_REPLY_CD_NOT_SUCCESS = "3024"
TEST_GET_INSTALL_RESP_REPLY_STR_NOT_SUCCESS = "Instalment not found (3024)"

TEST_GET_INSTALL_REQUEST_XML = f"""
                    <methods>
                        <GetInstalment>
                            <guid>{TEST_RESP_GUID}</guid>
                            <org_cd>{TEST_RESP_ORG}</org_cd>
                            <branch_cd>{TEST_RESP_BRANCH}</branch_cd>
                            <promissory_id>{TEST_PROMISSORY_ID}</promissory_id>
                            <inst_num>{TEST_INST_NUM}</inst_num>
                        </GetInstalment>
                    </methods>
                    """
TEST_GET_INSTALL_RESPONSE_XML_SUCCESS = f"""
                                <responses>
                                    <GetInstalment>
                                        <guid>{TEST_RESP_GUID}</guid>
                                        <org_cd>{TEST_RESP_ORG}</org_cd>
                                        <branch_cd>{TEST_RESP_BRANCH}</branch_cd>
                                        <promissory_id>{TEST_PROMISSORY_ID}</promissory_id>
                                        <inst_dt>{TEST_INST_DT}</inst_dt>
                                        <inst_num>{TEST_INST_NUM}</inst_num>
                                        <status>{EXPECTED_INSTALMENT_STATUS}</status>
                                        <reply_cd>{TEST_GET_INSTALL_RESP_REPLY_CD_SUCCESS}</reply_cd>
                                        <reply_str>{TEST_GET_INSTALL_RESP_REPLY_STR_SUCCESS}</reply_str>
                                    </GetInstalment>
                                </responses>
                            """

TEST_GET_INSTALL_RESPONSE_XML_INVALID = "<responses></responses>"

TEST_GET_INSTALL_RESPONSE_XML_ERROR_CODE = f"""
                                <responses>
                                    <GetInstalment>
                                        <guid>{TEST_RESP_GUID}</guid>
                                        <org_cd>{TEST_RESP_ORG}</org_cd>
                                        <branch_cd>{TEST_RESP_BRANCH}</branch_cd>
                                        <promissory_id>{TEST_PROMISSORY_ID}</promissory_id>
                                        <inst_dt>{TEST_INST_DT}</inst_dt>
                                        <inst_num>{TEST_INST_NUM}</inst_num>
                                        <reply_cd>{TEST_GET_INSTALL_RESP_REPLY_CD_NOT_SUCCESS}</reply_cd>
                                        <reply_str>{TEST_GET_INSTALL_RESP_REPLY_STR_NOT_SUCCESS}</reply_str>
                                    </GetInstalment>
                                </responses>
                                """


TEST_GET_INSTALL_RESPONSE_XML_MISSING_VALUES = f"""
                                <responses>
                                    <GetInstalment>
                                        <guid>{TEST_RESP_GUID}</guid>
                                        <org_cd>{TEST_RESP_ORG}</org_cd>
                                        <branch_cd>{TEST_RESP_BRANCH}</branch_cd>
                                        <promissory_id>{TEST_PROMISSORY_ID}</promissory_id>
                                        <inst_dt>{TEST_INST_DT}</inst_dt>
                                        <inst_num>{TEST_INST_NUM}</inst_num>
                                        <status></status>
                                        <reply_cd>{TEST_GET_INSTALL_RESP_REPLY_CD_SUCCESS}</reply_cd>
                                        <reply_str>{TEST_GET_INSTALL_RESP_REPLY_STR_SUCCESS}</reply_str>
                                    </GetInstalment>
                                </responses>
                            """


class TestGetInstalment(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from model.get_instalment import GetInstalment

        cls.GetInstalment = GetInstalment

    def setUp(self):
        self.get_instalment = self.GetInstalment(
            TEST_RESP_GUID, TEST_RESP_ORG, TEST_RESP_BRANCH, TEST_PROMISSORY_ID, TEST_INST_NUM
        )

    def test_init(self):
        self.assertEqual(self.get_instalment.guid, TEST_RESP_GUID)
        self.assertEqual(self.get_instalment.org_cd, TEST_RESP_ORG)
        self.assertEqual(self.get_instalment.branch_cd, TEST_RESP_BRANCH)
        self.assertEqual(self.get_instalment.promissory_id, TEST_PROMISSORY_ID)
        self.assertEqual(self.get_instalment.inst_num, TEST_INST_NUM)

    @patch("model.get_instalment.logger")
    def test_init_invalid_inst_num(self, mock_log):
        self.GetInstalment(TEST_RESP_GUID, TEST_RESP_ORG, TEST_RESP_BRANCH, TEST_PROMISSORY_ID, 1000)
        mock_log.error.assert_called_once()

    def test_to_xml(self):
        expected_xml = normalize_xml(TEST_GET_INSTALL_REQUEST_XML)
        self.assertEqual(normalize_xml(self.get_instalment.to_xml().strip()), expected_xml.strip())

    def test_xml_response_to_dict_successfull(self):
        xml_response = TEST_GET_INSTALL_RESPONSE_XML_SUCCESS
        expected_dict = {
            "responses": {
                "GetInstalment": {
                    "guid": TEST_RESP_GUID,
                    "org_cd": TEST_RESP_ORG,
                    "branch_cd": TEST_RESP_BRANCH,
                    "promissory_id": TEST_PROMISSORY_ID,
                    "inst_dt": TEST_INST_DT,
                    "inst_num": str(TEST_INST_NUM),
                    "status": EXPECTED_INSTALMENT_STATUS,
                    "reply_cd": TEST_GET_INSTALL_RESP_REPLY_CD_SUCCESS,
                    "reply_str": TEST_GET_INSTALL_RESP_REPLY_STR_SUCCESS,
                }
            }
        }
        self.assertDictEqual(self.get_instalment.xml_response_to_dict(xml_response), expected_dict)

    def test_xml_response_to_dict_with_invalid_xml(self):
        invalid_xml_response = TEST_GET_INSTALL_RESPONSE_XML_INVALID
        self.assertDictEqual(self.get_instalment.xml_response_to_dict(invalid_xml_response), {"responses": None})

    def test_xml_response_to_dict_with_error_code(self):
        xml_response = TEST_GET_INSTALL_RESPONSE_XML_ERROR_CODE
        expected_dict = {
            "responses": {
                "GetInstalment": {
                    "guid": TEST_RESP_GUID,
                    "org_cd": TEST_RESP_ORG,
                    "branch_cd": TEST_RESP_BRANCH,
                    "promissory_id": TEST_PROMISSORY_ID,
                    "inst_dt": TEST_INST_DT,
                    "inst_num": str(TEST_INST_NUM),
                    "reply_cd": TEST_GET_INSTALL_RESP_REPLY_CD_NOT_SUCCESS,
                    "reply_str": TEST_GET_INSTALL_RESP_REPLY_STR_NOT_SUCCESS,
                }
            }
        }
        self.assertDictEqual(self.get_instalment.xml_response_to_dict(xml_response), expected_dict)


class TestGetInstalmentResponseParser(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from model.get_instalment import GetInstalmentResponseParser

        cls.GetInstalmentResponseParser = GetInstalmentResponseParser

    def setUp(self):
        self.response_xml = TEST_GET_INSTALL_RESPONSE_XML_SUCCESS
        self.response_parser = self.GetInstalmentResponseParser(self.response_xml)

    def test_init(self):
        self.assertEqual(self.response_parser.response_xml, self.response_xml)

    def test_extract_values_successfull(self):
        self.assertEqual(self.response_parser.inst_dt, TEST_INST_DT)
        self.assertEqual(self.response_parser.status, EXPECTED_INSTALMENT_STATUS)
        self.assertEqual(self.response_parser.reply_cd, TEST_GET_INSTALL_RESP_REPLY_CD_SUCCESS)
        self.assertEqual(self.response_parser.reply_str, TEST_GET_INSTALL_RESP_REPLY_STR_SUCCESS)

    def test_extract_values_with_missing_info(self):
        xml_response_missing_info = TEST_GET_INSTALL_RESPONSE_XML_MISSING_VALUES
        response_parser_missing_info = self.GetInstalmentResponseParser(xml_response_missing_info)
        self.assertEqual(response_parser_missing_info.inst_dt, TEST_INST_DT)
        self.assertEqual(response_parser_missing_info.status, None)
        self.assertEqual(response_parser_missing_info.reply_cd, TEST_GET_INSTALL_RESP_REPLY_CD_SUCCESS)
        self.assertEqual(response_parser_missing_info.reply_str, TEST_GET_INSTALL_RESP_REPLY_STR_SUCCESS)

    @patch("model.get_instalment.logger")
    def test_extract_values_with_exception(self, mock_log):
        self.response_parser.response_dict = None  # This will cause an exception in extract_values
        self.response_parser.extract_values()
        mock_log.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
