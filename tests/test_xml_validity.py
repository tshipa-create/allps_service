import os
import sys
import unittest
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from test_get_instalment import (
    TEST_GET_INSTALL_REQUEST_XML,
    TEST_GET_INSTALL_RESPONSE_XML_SUCCESS,
    TEST_GET_INSTALL_RESPONSE_XML_INVALID,
    TEST_GET_INSTALL_RESPONSE_XML_ERROR_CODE,
    TEST_GET_INSTALL_RESPONSE_XML_MISSING_VALUES,
)
from test_open_asi import (
    TEST_OPEN_ASI_REQUEST_XML,
    TEST_OPEN_ASI_RESPONSE_XML_SUCCESS,
    TEST_OPEN_ASI_RESPONSE_XML_INVALID,
    TEST_OPEN_ASI_RESPONSE_XML_ERROR_CODE,
    TEST_OPEN_ASI_RESPONSE_XML_MISSING_VALUES,
)

from test_edit_instalment import (
    TEST_EDIT_INSTALL_REQUEST_XML,
    TEST_EDIT_INSTALL_RESPONSE_XML_SUCCESS,
    TEST_EDIT_INSTALL_RESPONSE_XML_INVALID,
    TEST_EDIT_INSTALL_RESPONSE_XML_ERROR_CODE,
    TEST_EDIT_INSTALL_RESPONSE_XML_MISSING_VALUES,
)


class TestXMLValidity(unittest.TestCase):
    """
    This test no the code but actual XML strings that are being used in Unit Tests.
    """

    def validate_xml_structure(self, xml_string):
        try:
            ET.fromstring(xml_string)
            return True
        except ET.ParseError:
            return False

    def test_xml_strings_are_well_formed(self):

        xml_test_get_instalment = {
            "TEST_GET_INSTALL_REQUEST_XML": TEST_GET_INSTALL_REQUEST_XML,
            "TEST_GET_INSTALL_RESPONSE_XML_SUCCESS": TEST_GET_INSTALL_RESPONSE_XML_SUCCESS,
            "TEST_GET_INSTALL_RESPONSE_XML_INVALID": TEST_GET_INSTALL_RESPONSE_XML_INVALID,
            "TEST_GET_INSTALL_RESPONSE_XML_ERROR_CODE": TEST_GET_INSTALL_RESPONSE_XML_ERROR_CODE,
            "TEST_GET_INSTALL_RESPONSE_XML_MISSING_VALUES": TEST_GET_INSTALL_RESPONSE_XML_MISSING_VALUES,
        }
        xml_test_open_asi = {
            "TEST_OPEN_ASI_REQUEST_XML": TEST_OPEN_ASI_REQUEST_XML,
            "TEST_OPEN_ASI_RESPONSE_XML_SUCCESS": TEST_OPEN_ASI_RESPONSE_XML_SUCCESS,
            "TEST_OPEN_ASI_RESPONSE_XML_INVALID": TEST_OPEN_ASI_RESPONSE_XML_INVALID,
            "TEST_OPEN_ASI_RESPONSE_XML_ERROR_CODE": TEST_OPEN_ASI_RESPONSE_XML_ERROR_CODE,
            "TEST_OPEN_ASI_RESPONSE_XML_MISSING_VALUES": TEST_OPEN_ASI_RESPONSE_XML_MISSING_VALUES,
        }
        xml_test_edit_instalment = {
            "TEST_EDIT_INSTALL_REQUEST_XML": TEST_EDIT_INSTALL_REQUEST_XML,
            "TEST_EDIT_INSTALL_RESPONSE_XML_SUCCESS": TEST_EDIT_INSTALL_RESPONSE_XML_SUCCESS,
            "TEST_EDIT_INSTALL_RESPONSE_XML_INVALID": TEST_EDIT_INSTALL_RESPONSE_XML_INVALID,
            "TEST_EDIT_INSTALL_RESPONSE_XML_ERROR_CODE": TEST_EDIT_INSTALL_RESPONSE_XML_ERROR_CODE,
            "TEST_EDIT_INSTALL_RESPONSE_XML_MISSING_VALUES": TEST_EDIT_INSTALL_RESPONSE_XML_MISSING_VALUES,
        }

        xml_strings = {**xml_test_edit_instalment, **xml_test_get_instalment, **xml_test_open_asi}
        for name, xml_str in xml_strings.items():
            with self.subTest(xml_var=name):
                self.assertTrue(self.validate_xml_structure(xml_str), f"{name} is not well-formed XML.")


if __name__ == "__main__":
    unittest.main()
