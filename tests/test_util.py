import sys
import os
import unittest
from unittest.mock import patch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from test_get_instalment import EXPECTED_INSTALMENT_STATUS
from tests.test_open_asi import (
    TEST_OPEN_ASI_RESPONSE_XML_SUCCESS,
    TEST_RESP_REPLY_CD_SUCCESS,
    TEST_RESP_REPLY_STR_SUCCESS,
    TEST_RESP_GUID,
)

from util import (
    get_reply_code_and_message,
    is_auth_guid,
    check_instalment_status,
    check_instalment_not_in_future,
    validate_full_instalment_info,
    installments_statistics_from_processings,
)

MEHTOD_NAME = "OpenAsi"
INSTALLMENT_STATUS_MISMATCH = "ACTIVE"
INSTALLMENT_STATUS_MATCH = "INCOMPLETE"


class TestUtilityFunctions(unittest.TestCase):

    def test_get_reply_code_and_message_success(self):
        xml_response = TEST_OPEN_ASI_RESPONSE_XML_SUCCESS
        code, message = get_reply_code_and_message(xml_response, MEHTOD_NAME)
        self.assertEqual(code, TEST_RESP_REPLY_CD_SUCCESS)
        self.assertEqual(message, TEST_RESP_REPLY_STR_SUCCESS)

    @patch("util.logger")
    def test_is_auth_guid_true(self, mock_log):
        self.assertTrue(is_auth_guid(TEST_RESP_GUID))
        mock_log.exception.assert_not_called()

    @patch("util.logger")
    def test_is_auth_guid_false(self, mock_log):
        self.assertFalse(is_auth_guid(None))
        mock_log.exception.assert_called_once()

    @patch("util.logger")
    def test_check_instalment_status_mismatch(self, mock_log):
        self.assertFalse(check_instalment_status(INSTALLMENT_STATUS_MISMATCH, EXPECTED_INSTALMENT_STATUS))
        mock_log.info.assert_called_once()

    @patch("util.logger")
    def test_check_instalment_not_in_future_future_date(self, mock_log):
        future_date = "20991231"
        self.assertFalse(check_instalment_not_in_future(future_date))
        mock_log.info.assert_called_once()

    def test_validate_full_instalment_info_valid(self):
        installment_date = "20240101"
        self.assertTrue(
            validate_full_instalment_info(INSTALLMENT_STATUS_MATCH, EXPECTED_INSTALMENT_STATUS, installment_date)
        )

    def test_installments_statistics_from_processings_no_installments(self):
        with patch("util.logger") as mock_log:
            installments_statistics_from_processings(0, 0)
            mock_log.warning.assert_called_with("RUN STATISTICS: No instalments to edit")

    def test_installments_statistics_from_processings_all_installments_edited(self):
        with patch("util.logger") as mock_log:
            installments_statistics_from_processings(3, 3)
            mock_log.info.assert_called_with("RUN STATISTICS: All instalments were edited")

    def test_installments_statistics_from_processings_mismatch(self):
        with patch("util.logger") as mock_log:
            installments_statistics_from_processings(3, 2)
            mock_log.warning.assert_called_with(
                f"RUN STATISTICS: Mismatch between total instalments: {3} and edited instalments: {2}"
            )


if __name__ == "__main__":
    unittest.main()
