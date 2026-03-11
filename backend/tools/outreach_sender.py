from backend.services.llm_service import call_llm
from backend.services.email_service import send_email


def run(company: str, email: str, icp: str, signals: list, account_brief: str):
    """
    Generate personalized outreach email and send it.
    """

    system_prompt = """
You are a B2B sales outreach specialist.

Write a short, highly personalized cold outreach email.

Rules:
- Reference the company's signals explicitly.
- Connect those signals to the product in the ICP.
- Be professional and concise.
- Include a clear call to action.
"""

    user_prompt = f"""
Company: {company}

ICP:
{icp}

Signals:
{signals}

Account Brief:
{account_brief}

Write an outreach email.
Include a subject line and body.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = call_llm(messages)

    email_content = response.get("content", "")

    # Basic subject/body split
    subject = f"Helping {company} scale securely"
    body = email_content

    result = send_email(email, subject, body)

    return {
        "company": company,
        "email": email,
        "subject": subject,
        "body": body,
        "delivery_status": result
    }