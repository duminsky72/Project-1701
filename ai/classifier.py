def classify_alarm(alarm: dict) -> dict:
    """
    AI / rule-based alarm classification
    Replace this with OpenAI or Bedrock later
    """

    # Basic rules (safe default)
    if alarm["state"] == "ALARM":
        severity = "CRITICAL"
        suppress = False
    else:
        severity = "INFO"
        suppress = True

    message = (
        f"🚨 {severity} – {alarm['alarm_name']}\n"
        f"Service: {alarm['service']}\n"
        f"Region: {alarm['region']}\n"
        f"Reason: {alarm['reason']}"
    )

    return {
        "severity": severity,
        "suppress": suppress,
        "message": message
    }
