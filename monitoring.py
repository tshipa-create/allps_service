from logger_config import logger
from db import fetch_daily_monitoring_data, find_retry_responses
import config
from slack_integration import slack_post_msg, slack_post_file


def main():

    if config.ENABLE_SLACK_NOTIFICATIONS:
        logger.info("Running monitoring")
        df_monitoring = fetch_daily_monitoring_data()
        if df_monitoring is not None:
            slack_post_msg(df_monitoring)

        df_responses = find_retry_responses()
        if df_responses is not None:
            total = len(df_responses)
            edited_df = df_responses[df_responses["amt_pct"].notnull()]
            edited: int = len(edited_df)
            success: int = len(edited_df[edited_df["success"] == True])
            rate = 0
            if edited > 0:
                rate = int(success / edited * 100)
            msg = f"""
            *ALLPS instalment retry summary*
            Total processed: {total}
            Instalments edited: {edited}, skipped: {total - edited}
            Instalments successfully edited: {success}/{edited} ({rate}%)
            """

            key = "VIEW_RETRY_RESPONSES"

            slack_post_file(msg, key, df_responses)
    else:
        logger.info("Skipping monitoring, Slack notifications disabled")


if __name__ == "__main__":
    main()
