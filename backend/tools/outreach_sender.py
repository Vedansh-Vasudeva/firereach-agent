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
- Return valid JSON with keys: subject, body, html
"""

    user_prompt = f"""
Company: {company}

ICP:
{icp}

Signals:
{signals}

Account Brief:
{account_brief}

Write the email now.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = call_llm(messages)

    subject = response.get("subject") or f"Security training for {company}'s next growth phase"
    body = response.get("body") or response.get("content", "").strip()
    html = response.get("html") or body.replace("\n", "<br>")

    if not body:
        body = (
            f"I noticed {company} is showing recent growth activity, including {', '.join(signal.get('label', '') for signal in signals[:2])}. "
            f"Teams in that stage often need stronger security habits as headcount and systems expand.\n\n"
            f"We help companies that fit this ICP: {icp}. If it would be useful, I can share how similar teams turn rapid expansion into practical security training rollouts."
        )
        html = body.replace("\n", "<br>")

    result = send_email(email, subject, html)

    return {
        "company": company,
        "email": email,
        "subject": subject,
        "body": body,
        "html": html,
        "delivery_status": result
    }
