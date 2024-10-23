# ALLPS Service

## Description

This service uses Snowflake pre-defined views and queries to get installments data to be modified in ALLPS with their API. In short, idea is to retry payments for the loans which did not get paid in the first attempt.

Uses Snowflake Views of ```VIEW_ALLPS_RETRY_INSTALMENTS``` to get raw retry installments data, then filter it and save it to Snowflake table ```RAW_RETRY_LOANS_DATA```.
XML logs are saved to ```ALLPS_SERVICE_API_LOGS``` Snowflake table

For Slack monitoring data from Snowflake tables ```VIEW_RETRY_RESPONSES```, ```ALLPS_SERVICE_API_LOGS``` and ```EDIT_INSTALMENT_LOG``` are used.
