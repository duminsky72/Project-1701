from aggregation import should_aggregate

def handler(event, context):
    alarm = parse_cloudwatch_event(event)

    if should_aggregate(alarm):
        return {"status": "aggregated"}

    decision = classify_alarm(alarm)

    if decision["suppress"]:
        return {"status": "suppressed"}

    contacts = get_contacts(decision["severity"], alarm["service"])

    for c in contacts:
        if "SMS" in c["channels"]:
            send_sms(c["phone"], decision["message"])
        if "WHATSAPP" in c["channels"]:
            send_whatsapp(c["whatsapp"], decision["message"])

    return {"status": "sent"}
