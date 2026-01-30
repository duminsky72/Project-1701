import json
from cloudwatch import parse_cloudwatch_event
from ai.classifier import classify_alarm
from db.aurora import get_contacts
from notify.sms import send_sms
from notify.whatsapp import send_whatsapp


def handler(event, context):
    """
    AWS Lambda entrypoint
    Triggered by EventBridge or SNS from CloudWatch
    """

    alarm = parse_cloudwatch_event(event)

    decision = classify_alarm(alarm)

    if decision["suppress"]:
        return {"status": "suppressed"}

    contacts = get_contacts(
        severity=decision["severity"],
        service=alarm["service"]
    )

    for contact in contacts:
        if "SMS" in contact["channels"]:
            send_sms(contact["phone"], decision["message"])

        if "WHATSAPP" in contact["channels"]:
            send_whatsapp(contact["whatsapp"], decision["message"])

    return {"status": "sent"}
