import os
import time
import boto3

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["AGG_TABLE"])

AGG_WINDOW_SECONDS = 300  # 5 minutes


def should_aggregate(alarm: dict) -> bool:
    key = f"{alarm['alarm_name']}:{alarm['region']}"
    now = int(time.time())

    try:
        table.put_item(
            Item={
                "alarm_key": key,
                "last_seen": now,
                "expires_at": now + AGG_WINDOW_SECONDS
            },
            ConditionExpression="attribute_not_exists(alarm_key)"
        )
        return False  # first occurrence
    except Exception:
        return True  # duplicate within window
