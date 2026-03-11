from backend.services.llm_service import call_llm


def run(company: str, icp: str, signals: list):
    """
    Generates a strategic account brief based on company signals and ICP.
    """

    system_prompt = """
You are an expert B2B sales research analyst.

Your job is to analyze a company based on detected growth signals
and an Ideal Customer Profile (ICP).

Write a concise 2-paragraph account brief explaining:

1) What the company's recent signals indicate about their growth stage.
2) Why this company would benefit from the product described in the ICP.

Be specific and strategic.
Do NOT invent signals beyond the ones provided.
"""

    user_prompt = f"""
Company: {company}

ICP:
{icp}

Detected Signals:
{signals}

Write a 2 paragraph account brief explaining why this company
is a good fit for the ICP solution.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = call_llm(messages)

    return {
        "company": company,
        "account_brief": response.get("content", "")
    }