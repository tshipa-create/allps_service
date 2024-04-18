import traceback
import requests
import config
from logger_config import logger
import pandas as pd
from collections import defaultdict


def format_slack_message(df):
    grouped = (
        df.groupby(["HOST", "METHOD_NAME", "RESPONSE_CODE", "RESPONSE_MESSAGE"])["COUNT_OF_ROWS"].sum().reset_index()
    )

    summary = defaultdict(lambda: defaultdict(list))
    for _, row in grouped.iterrows():
        summary[row["HOST"]][row["METHOD_NAME"]].append(
            (row["RESPONSE_CODE"], row["RESPONSE_MESSAGE"], row["COUNT_OF_ROWS"])
        )

    message_lines = [f"*Daily API Monitoring Report for {df['MONITORING_DATE'].iloc[0]}*"]
    for host, methods in summary.items():
        message_lines.append(f"*Host:* {host}")
        for method, responses in methods.items():
            message_lines.append(f"    • *Method:* {method}")
            response_lines = [f"        ◦ `{resp[0]}`: {resp[2]} - _{resp[1]}_" for resp in responses]
            message_lines.extend(response_lines)

    message = "\n".join(message_lines)
    slack_message = {"text": message}
    return slack_message


def slack_post_msg(df: pd.DataFrame):
    slack_webhook_url = "https://hooks.slack.com/services/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"
    if not df.empty:
        formatted_message = format_slack_message(df)
        message = {"channel": "#data_team_allps_service", "username": "awsbot", "text": formatted_message["text"]}
        try:
            response = requests.post(slack_webhook_url, json=message, timeout=config.SLACK_TIMEOUT)
            logger.info(f"Slack message posted to {slack_webhook_url} with response: {response.text}")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.exception(f"Error posting message to Slack: {e}")
            traceback.print_exc()
