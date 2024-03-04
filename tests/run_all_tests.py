import unittest
from test_open_asi import TestOpenAsi, TestOpenAsiResponseParser
from test_util import TestUtilityFunctions

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestOpenAsi))
    suite.addTests(loader.loadTestsFromTestCase(TestOpenAsiResponseParser))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
