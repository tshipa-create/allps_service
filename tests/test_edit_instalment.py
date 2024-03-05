import os
import sys
import unittest
from unittest.mock import patch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from main import EXPECTED_INSTALMENT_STATUS
from model.edit_instalment import EditInstalment, EditInstalmentResponseParser
from test_open_asi import TEST_RESP_GUID, TEST_RESP_ORG, TEST_RESP_BRANCH, normalize_xml
from test_get_instalment import TEST_PROMISSORY_ID, TEST_INST_NUM


TEST_EDIT_INSTALL_ACTION_DT = "20240130"
TEST_EDIT_INSTALL_IVALID_DATE_FORMAT = "2024-01-30"
TEST_EDIT_INSTALL_RESP_REPLY_CD_SUCCESS = "207"
TEST_EDIT_INSTALL_RESP_REPLY_STR_SUCCESS = "Transaction Successful (207)"
TEST_EDIT_INSTALL_RESP_REPLY_CD_NOT_SUCCESS = "341"
TEST_EDIT_INSTALL_RESP_REPLY_STR_NOT_SUCCESS = "More than 2 arrears collections in same cycle not allowed (341)"

TEST_EDIT_INSTALL_REQUEST_XML = f"""
        <methods>
            <EditInstalment>
                <guid>{TEST_RESP_GUID}</guid>
                <org_cd>{TEST_RESP_ORG}</org_cd>
                <branch_cd>{TEST_RESP_BRANCH}</branch_cd>
                <promissory_id>{TEST_PROMISSORY_ID}</promissory_id>
                <inst_num>{TEST_INST_NUM}</inst_num>
                <new_action_dt>{TEST_EDIT_INSTALL_ACTION_DT}</new_action_dt>
            </EditInstalment>
        </methods>
        """

TEST_EDIT_INSTALL_RESPONSE_XML_SUCCESS = f"""
        <responses>
            <EditInstalment>
                <guid>{TEST_RESP_GUID}</guid>
                <org_cd>{TEST_RESP_ORG}</org_cd>
                <branch_cd>{TEST_RESP_BRANCH}</branch_cd>
                <promissory_id>{TEST_PROMISSORY_ID}</promissory_id>
                <inst_num>{TEST_INST_NUM}</inst_num>
                <new_action_dt>{TEST_EDIT_INSTALL_ACTION_DT}</new_action_dt>
                <status>{EXPECTED_INSTALMENT_STATUS}</status>
                <reply_cd>{TEST_EDIT_INSTALL_RESP_REPLY_CD_SUCCESS}</reply_cd>
                <reply_str>{TEST_EDIT_INSTALL_RESP_REPLY_STR_SUCCESS}</reply_str>
            </EditInstalment>
        </responses>
        """

TEST_EDIT_INSTALL_RESPONSE_XML_INVALID = "<responses></responses>"

TEST_EDIT_INSTALL_RESPONSE_XML_ERROR_CODE = f"""
        <responses>
            <EditInstalment>
                <guid>{TEST_RESP_GUID}</guid>
                <org_cd>{TEST_RESP_ORG}</org_cd>
                <branch_cd>{TEST_RESP_BRANCH}</branch_cd>
                <promissory_id>{TEST_PROMISSORY_ID}</promissory_id>
                <inst_num>{TEST_INST_NUM}</inst_num>
                <new_action_dt></new_action_dt>
                <reply_cd>{TEST_EDIT_INSTALL_RESP_REPLY_CD_SUCCESS}</reply_cd>
                <reply_str>{TEST_EDIT_INSTALL_RESP_REPLY_STR_SUCCESS}</reply_str>
            </EditInstalment>
        </responses>
        """

TEST_EDIT_INSTALL_RESPONSE_XML_MISSING_VALUES = f"""
        <responses>
            <EditInstalment>
                <guid>{TEST_RESP_GUID}</guid>
                <org_cd>{TEST_RESP_ORG}</org_cd>
                <branch_cd>{TEST_RESP_BRANCH}</branch_cd>
                <promissory_id>{TEST_PROMISSORY_ID}</promissory_id>
                <inst_num>{TEST_INST_NUM}</inst_num>
                <new_action_dt></new_action_dt>
                <reply_cd>{TEST_EDIT_INSTALL_RESP_REPLY_CD_NOT_SUCCESS}</reply_cd>
                <reply_str>{TEST_EDIT_INSTALL_RESP_REPLY_STR_NOT_SUCCESS}</reply_str>
            </EditInstalment>
        </responses>
        """


class TestEditInstalment(unittest.TestCase):
    def setUp(self):
        self.guid = TEST_RESP_GUID
        self.org_cd = TEST_RESP_ORG
        self.branch_cd = TEST_RESP_BRANCH
        self.promissory_id = TEST_PROMISSORY_ID
        self.inst_num = TEST_INST_NUM
        self.new_action_dt = TEST_EDIT_INSTALL_ACTION_DT
        self.edit_instalment = EditInstalment(
            self.guid, self.org_cd, self.branch_cd, self.promissory_id, self.inst_num, self.new_action_dt
        )

    def test_init(self):
        self.assertEqual(self.edit_instalment.guid, self.guid)
        self.assertEqual(self.edit_instalment.org_cd, self.org_cd)
        self.assertEqual(self.edit_instalment.branch_cd, self.branch_cd)
        self.assertEqual(self.edit_instalment.promissory_id, self.promissory_id)
        self.assertEqual(self.edit_instalment.inst_num, self.inst_num)
        self.assertEqual(self.edit_instalment.new_action_dt, self.new_action_dt)

    @patch("model.edit_instalment.logObject")
    def test_init_invalid_inst_num(self, mock_log):
        EditInstalment(self.guid, self.org_cd, self.branch_cd, self.promissory_id, 1000, self.new_action_dt)
        mock_log.error.assert_called_once()

    @patch("model.edit_instalment.logObject")
    def test_init_invalid_date(self, mock_log):
        EditInstalment(
            self.guid,
            self.org_cd,
            self.branch_cd,
            self.promissory_id,
            self.inst_num,
            TEST_EDIT_INSTALL_IVALID_DATE_FORMAT,
        )
        mock_log.error.assert_called_once()

    def test_to_xml(self):
        expected_xml = normalize_xml(TEST_EDIT_INSTALL_REQUEST_XML)
        self.assertEqual(normalize_xml(self.edit_instalment.to_xml().strip()), expected_xml.strip())

    def test_xml_response_to_dict_successfull(self):
        xml_response = TEST_EDIT_INSTALL_RESPONSE_XML_SUCCESS
        expected_dict = {
            "responses": {
                "EditInstalment": {
                    "guid": self.guid,
                    "org_cd": self.org_cd,
                    "branch_cd": self.branch_cd,
                    "promissory_id": self.promissory_id,
                    "inst_num": str(self.inst_num),
                    "new_action_dt": self.new_action_dt,
                    "status": EXPECTED_INSTALMENT_STATUS,
                    "reply_cd": TEST_EDIT_INSTALL_RESP_REPLY_CD_SUCCESS,
                    "reply_str": TEST_EDIT_INSTALL_RESP_REPLY_STR_SUCCESS,
                }
            }
        }
        self.assertDictEqual(self.edit_instalment.xml_response_to_dict(xml_response), expected_dict)

    def test_xml_response_to_dict_with_invalid_xml(self):
        invalid_xml_response = TEST_EDIT_INSTALL_RESPONSE_XML_INVALID
        self.assertDictEqual(self.edit_instalment.xml_response_to_dict(invalid_xml_response), {"responses": None})

    def test_xml_response_to_dict_with_error_code(self):
        xml_response = TEST_EDIT_INSTALL_RESPONSE_XML_ERROR_CODE
        excepted_dict = {
            "responses": {
                "EditInstalment": {
                    "guid": self.guid,
                    "org_cd": self.org_cd,
                    "branch_cd": self.branch_cd,
                    "promissory_id": self.promissory_id,
                    "inst_num": str(self.inst_num),
                    "new_action_dt": None,
                    "reply_cd": TEST_EDIT_INSTALL_RESP_REPLY_CD_SUCCESS,
                    "reply_str": TEST_EDIT_INSTALL_RESP_REPLY_STR_SUCCESS,
                }
            }
        }
        self.assertDictEqual(self.edit_instalment.xml_response_to_dict(xml_response), excepted_dict)


class TestEditInstalmentResponseParser(unittest.TestCase):
    def setUp(self):
        self.response_xml = TEST_EDIT_INSTALL_RESPONSE_XML_SUCCESS
        self.response_parser = EditInstalmentResponseParser(self.response_xml)

    def test_extract_values(self):
        self.assertEqual(self.response_parser.inst_num, str(TEST_INST_NUM))
        self.assertEqual(self.response_parser.new_action_dt, TEST_EDIT_INSTALL_ACTION_DT)
        self.assertEqual(self.response_parser.reply_cd, TEST_EDIT_INSTALL_RESP_REPLY_CD_SUCCESS)
        self.assertEqual(self.response_parser.reply_str, TEST_EDIT_INSTALL_RESP_REPLY_STR_SUCCESS)

    def test_extract_values_with_missing_info(self):
        response_parser = EditInstalmentResponseParser(TEST_EDIT_INSTALL_RESPONSE_XML_MISSING_VALUES)
        self.assertEqual(response_parser.inst_num, str(TEST_INST_NUM))
        self.assertEqual(response_parser.new_action_dt, None)
        self.assertEqual(response_parser.reply_cd, TEST_EDIT_INSTALL_RESP_REPLY_CD_NOT_SUCCESS)
        self.assertEqual(response_parser.reply_str, TEST_EDIT_INSTALL_RESP_REPLY_STR_NOT_SUCCESS)

    @patch("model.edit_instalment.logObject")
    def test_extract_values_with_exception(self, mock_log):
        self.response_parser.response_dict = None  # This will cause an exception in extract_values
        self.response_parser.extract_values()
        mock_log.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
