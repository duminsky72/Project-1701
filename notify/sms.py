import boto3

sns = boto3.client("sns")


def send_sms(phone: str, message: str):
    sns.publish(
        PhoneNumber=phone,
        Message=message
    )
