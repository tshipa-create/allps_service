from logger_config import logger
from db import (
    fetch_daily_monitoring_data,
)
import config
from slack_integration import slack_post_msg


def main():

    if config.ENABLE_SLACK_NOTIFICATIONS:
        logger.info("Running monitoring")
        df_monitoring = fetch_daily_monitoring_data()
        if df_monitoring:
            slack_post_msg(df_monitoring)
    else:
        logger.info("Skipping monitoring, Slack notifications disabled")


if __name__ == "__main__":
    main()
