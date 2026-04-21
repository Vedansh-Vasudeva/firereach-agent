import requests
from backend.config import config


RESEND_API_URL = "https://api.resend.com/emails"


def send_email(to_email: str, subject: str, content: str):
    """
    Sends email using Resend API.
    """

    if not config.RESEND_API_KEY:
        return {
            "status": "skipped",
            "reason": "RESEND_API_KEY is not configured.",
        }

    headers = {
        "Authorization": f"Bearer {config.RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "from": "FireReach <onboarding@resend.dev>",
        "to": [to_email],
        "subject": subject,
        "html": content
    }

    try:

        response = requests.post(
            RESEND_API_URL,
            headers=headers,
            json=data
        )

        if response.ok:
            return {
                "status": "sent",
                "status_code": response.status_code,
                "response": response.json() if response.text else {},
            }

        return {
            "status": "failed",
            "status_code": response.status_code,
            "response": response.text,
        }

    except Exception as e:

        return {
            "status": "failed",
            "error": str(e)
        }
