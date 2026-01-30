import os
import json
import boto3
import requests

AI_PROVIDER = os.getenv("AI_PROVIDER", "BEDROCK")  # BEDROCK | OPENAI

# ---------- BEDROCK ----------
bedrock = boto3.client("bedrock-runtime")

def classify_with_bedrock(alarm: dict) -> dict:
    prompt = f"""
You are an on-call SRE.
Classify the following AWS alarm.

Alarm name: {alarm['alarm_name']}
Service: {alarm['service']}
Region: {alarm['region']}
Reason: {alarm['reason']}

Return JSON with:
severity: INFO | WARNING | CRITICAL
suppress: true | false
summary: short human readable message
"""

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps({
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300
        })
    )

    result = json.loads(response["body"].read())
    return json.loads(result["content"][0]["text"])


# ---------- OPENAI ----------
def classify_with_openai(alarm: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{
            "role": "user",
            "content": f"""
Classify this AWS alarm and return JSON only.

Alarm: {alarm}
Fields: severity, suppress, summary
"""
        }]
    }

    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=10
    )

    return json.loads(r.json()["choices"][0]["message"]["content"])


# ---------- ENTRY ----------
def classify_alarm(alarm: dict) -> dict:
    try:
        if AI_PROVIDER == "OPENAI":
            decision = classify_with_openai(alarm)
        else:
            decision = classify_with_bedrock(alarm)
    except Exception:
        # Safe fallback
        decision = {
            "severity": "CRITICAL",
            "suppress": False,
            "summary": f"Alarm triggered: {alarm['alarm_name']}"
        }

    message = (
        f"🚨 {decision['severity']} – {alarm['alarm_name']}\n"
        f"{decision['summary']}\n"
        f"Region: {alarm['region']}"
    )

    return {
        "severity": decision["severity"],
        "suppress": decision["suppress"],
        "message": message
    }
