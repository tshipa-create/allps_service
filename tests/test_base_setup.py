import unittest
from unittest.mock import patch


class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        patcher = patch.dict(
            "os.environ",
            {
                "SF_ACCOUNT": "mock_account",
                "SF_USER": "mock_user",
                "SF_PASSWORD": "mock_password",
                "SF_DATABASE_NAME": "mock_database",
                "SF_SCHEMA_NAME": "mock_schema",
                "SF_ALLPS_XML_LOG_TABLE": "mock_table",
                "ALLPS_HOST": "mock_host",
                "ALLPS_USER": "mock_user",
                "ALLPS_PASSWORD": "mock",
                "ALLPS_MACHINE_NAME": "mock_machine",
                "ALLPS_USER_IF": "mock_user_if",
                "ALLPS_INTEGRATOR": "mock_integrator",
                "ALLPS_PRODUCT": "mock_product",
                "ALLPS_PRODUCT_VERSION": "mock_version",
                "ALLPS_ORG_CODE": "mock_org",
                "ALLPS_BRANCH_CODE": "mock_branch",
                "ALLPS_NEW_TRACK_CODE": "07",
                "SLACK_TIMEOUT": "60",
                "ENABLE_SLACK_NOTIFICATIONS": "mock_enable",
                "ALLPS_RESPONSE_CODES_RETRY_LIST": "1800, 331",
            },
        )
        cls.env_patcher = patcher.start()
