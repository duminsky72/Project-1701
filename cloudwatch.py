def parse_cloudwatch_event(event: dict) -> dict:
    """
    Normalizes CloudWatch / EventBridge events
    """

    detail = event.get("detail", {})

    return {
        "alarm_name": detail.get("alarmName"),
        "state": detail.get("state", {}).get("value"),
        "reason": detail.get("state", {}).get("reason"),
        "service": detail.get("configuration", {})
                         .get("metrics", [{}])[0]
                         .get("metricStat", {})
                         .get("metric", {})
                         .get("namespace", "unknown"),
        "region": event.get("region"),
        "timestamp": event.get("time")
    }
