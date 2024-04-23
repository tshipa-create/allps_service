from os import environ, path
import json
from dotenv import load_dotenv

working_directory = path.dirname(__file__)
dotenv_path = path.join(working_directory, ".env")
# Overwrite existing environment variables with values from .env file
# Workaround as I couldn't get the .env envrionment variables to laod changes properly in the IDE
load_dotenv(dotenv_path, override=True)

SF_ACCOUNT = environ["SF_ACCOUNT"]
SF_USER = environ["SF_USER"]
SF_PASSWORD = environ["SF_PASSWORD"]
SF_DATABASE = environ["SF_DATABASE_NAME"]
SF_SCHEMA = environ["SF_SCHEMA_NAME"]
SF_ALLPS_XML_LOG_TABLE = environ["SF_ALLPS_XML_LOG_TABLE"]

ALLPS_HOST = environ["ALLPS_HOST"]
ALLPS_USER = environ["ALLPS_USER"]
ALLPS_PASSWORD = environ["ALLPS_PASSWORD"]
ALLPS_MACHINE_NAME = environ["ALLPS_MACHINE_NAME"]
ALLPS_USER_IF = environ["ALLPS_USER_IF"]
ALLPS_INTEGRATOR = environ["ALLPS_INTEGRATOR"]
ALLPS_PRODUCT = environ["ALLPS_PRODUCT"]
ALLPS_PRODUCT_VERSION = environ["ALLPS_PRODUCT_VERSION"]
ALLPS_ORG_CODE = environ["ALLPS_ORG_CODE"]
ALLPS_BRANCH_CODE = environ["ALLPS_BRANCH_CODE"]
ALLPS_NEW_TRACK_CODE = environ["ALLPS_NEW_TRACK_CODE"]
ALLPS_RESPONSE_CODES_RETRY_LIST = [item.strip() for item in environ["ALLPS_RESPONSE_CODES_RETRY_LIST"].split(",")]

SLACK_TIMEOUT = int(environ["SLACK_TIMEOUT"])
ENABLE_SLACK_NOTIFICATIONS = bool(environ.get("ENABLE_SLACK_NOTIFICATIONS", False).lower() == "true")

RAW_RETRY_LOANDS_FILTERS_JSON = json.loads(environ["RAW_RETRY_LOANDS_FILTERS_JSON"])