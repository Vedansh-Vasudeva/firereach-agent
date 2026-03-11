from backend.services.serp_service import search_google


def detect_signal(text: str):
    """
    Simple keyword-based signal detection.
    """

    signals = []

    text_lower = text.lower()

    if "funding" in text_lower or "series" in text_lower:
        signals.append("Recent funding round")

    if "hiring" in text_lower or "job" in text_lower:
        signals.append("Hiring expansion")

    if "cto" in text_lower or "ceo" in text_lower or "leadership" in text_lower:
        signals.append("Leadership change")

    if "expansion" in text_lower or "growth" in text_lower:
        signals.append("Company expansion")

    return signals


def run(company: str):
    """
    Harvest growth signals for a given company.
    """

    query = f"{company} funding OR hiring OR expansion OR CTO"

    results = search_google(query)

    detected_signals = []

    for result in results:
        text = f"{result.get('title','')} {result.get('snippet','')}"

        signals = detect_signal(text)

        detected_signals.extend(signals)

    # Remove duplicates
    detected_signals = list(set(detected_signals))

    return {
        "company": company,
        "signals": detected_signals
    }