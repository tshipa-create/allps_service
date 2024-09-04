from logger_config import logger
from db import fetch_daily_monitoring_data, find_retry_responses
import config
from slack_integration import slack_post_msg, slack_post_file


def main():

    if config.ENABLE_SLACK_NOTIFICATIONS:
        logger.info("Running monitoring")
        df_monitoring = fetch_daily_monitoring_data()
        if df_monitoring:
            slack_post_msg(df_monitoring)

        df_responses = find_retry_responses()
        if df_responses is not None:
            total = len(df_responses)
            success: int = len(df_responses[df_responses["success"] == True])
            rate = int(success / total * 100)
            msg = f"""
            *ALLPS instalment retry summary*
            Total retries: {total}
            Instalments successfully edited: {success}/{total} ({rate}%)
            """
            key = "VIEW_RETRY_RESPONSES"

            slack_post_file(msg, key, df_responses)
    else:
        logger.info("Skipping monitoring, Slack notifications disabled")


if __name__ == "__main__":
    main()
