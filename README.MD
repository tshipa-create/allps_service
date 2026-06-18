  # ALLPS Instalment Retry Service

  Automated service that retries failed loan instalment payments in the ALLPS loan management system. Runs on a schedule, identifies instalments that failed
   on their first attempt, and resubmits them with updated action dates — reducing manual collections work.

  ## What it does

  1. Queries `VIEW_ALLPS_RETRY_INSTALMENTS` in Snowflake to get failed instalments
  2. Applies date-window filters (`RAW_RETRY_LOANS_FILTERS_JSON`) to target the right payment cycles
  3. For each eligible instalment:
     - Validates status is `INCOMPLETE` with a valid amount and date
     - If full amount (`AMT_PCT == 100`): calls ALLPS API directly to update the action date
     - If partial (`AMT_PCT < 100`): invokes `allps_instalment_api` Lambda asynchronously with split payment details
  4. Saves results to `RAW_RETRY_LOANS_DATA` in Snowflake
  5. Posts a run summary to Slack

  ## Tech Stack

  | Component | Technology |
  |---|---|
  | Language | Python |
  | Data warehouse | Snowflake (SQLAlchemy + private key auth via SSM) |
  | External API | ALLPS SOAP/XML API |
  | AWS | Lambda (async invocation), SSM Parameter Store |
  | Monitoring | Slack notifications |
  | CI/CD | Bitbucket Pipelines + AWS CodeDeploy |

  ## Snowflake Tables

  | Table / View | Purpose |
  |---|---|
  | `VIEW_ALLPS_RETRY_INSTALMENTS` | Input — instalments to retry |
  | `RAW_RETRY_LOANS_DATA` | Output — processed results |
  | `ALLPS_SERVICE_API_LOGS` | SOAP request/response audit log |
  | `EDIT_INSTALMENT_LOG` | Instalment edit history |
  | `VIEW_RETRY_RESPONSES` | Slack monitoring feed |

  ## Configuration

  Copy `.env_SAMPLE` to `.env` and populate:

  SF_ACCOUNT=
  SF_USER=
  SF_DATABASE=
  SF_SCHEMA=
  SF_WAREHOUSE=
  SLACK_BOT_TOKEN=
  SLACK_CHANNEL_ID=
  RAW_RETRY_LOANS_FILTERS_JSON=

  AWS SSM provides Snowflake private key (`/snowflake/connection_private_key`) and passphrase.

  ## Running Locally

  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  python main.py

  Testing

  python -m pytest tests/ -v

  11 test files covering core filtering logic, API response handling, and Snowflake write operations.
