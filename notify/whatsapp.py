import os
import requests


def send_whatsapp(number: str, message: str):
    """
    Twilio WhatsApp API
    """

    url = f"https://api.twilio.com/2010-04-01/Accounts/{os.environ['TWILIO_SID']}/Messages.json"

    payload = {
        "From": f"whatsapp:{os.environ['TWILIO_WHATSAPP_FROM']}",
        "To": f"whatsapp:{number}",
        "Body": message
    }

    response = requests.post(
        url,
        data=payload,
        auth=(os.environ["TWILIO_SID"], os.environ["TWILIO_TOKEN"])
    )

    response.raise_for_status()
