import unittest
from test_open_asi import TestOpenAsi, TestOpenAsiResponseParser
from test_util import TestUtilityFunctions
from test_service_client import TestServiceClient
from test_edit_instalment import TestEditInstalment, TestEditInstalmentResponseParser
from test_get_instalment import TestGetInstalment, TestGetInstalmentResponseParser
from test_xml_validity import TestXMLValidity
from test_allps_service import TestAllpsService
from test_logger_config import TestLoggerConfig

if __name__ == "__main__":
    print("Running all tests...")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestOpenAsi))
    suite.addTests(loader.loadTestsFromTestCase(TestOpenAsiResponseParser))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestServiceClient))
    suite.addTests(loader.loadTestsFromTestCase(TestGetInstalment))
    suite.addTests(loader.loadTestsFromTestCase(TestGetInstalmentResponseParser))
    suite.addTests(loader.loadTestsFromTestCase(TestEditInstalment))
    suite.addTests(loader.loadTestsFromTestCase(TestEditInstalmentResponseParser))
    suite.addTests(loader.loadTestsFromTestCase(TestXMLValidity))
    suite.addTests(loader.loadTestsFromTestCase(TestAllpsService))
    suite.addTests(loader.loadTestsFromTestCase(TestLoggerConfig))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
