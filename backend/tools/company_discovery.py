import re
from backend.services.serp_service import search_google


def extract_company_names(text):
    """
    Very simple heuristic to extract possible company names
    from search results.
    """

    pattern = r"\b[A-Z][a-zA-Z]+\b"
    matches = re.findall(pattern, text)

    return list(set(matches))


def run(icp: str):
    """
    Discover companies that match the ICP and show growth signals.
    """

    query = f"{icp} startup funding OR hiring OR expansion"

    search_results = search_google(query)

    companies = set()

    for result in search_results:
        title = result.get("title", "")
        snippet = result.get("snippet", "")

        text = f"{title} {snippet}"

        names = extract_company_names(text)

        for name in names:
            companies.add(name)

    companies = list(companies)

    return {
        "companies": companies[:5]
    }