import re
from backend.services.serp_service import search_google


def extract_domain(company: str):
    """
    Attempts to find the company's website domain using Google search.
    """

    query = f"{company} official website"

    results = search_google(query)

    for result in results:
        link = result.get("link", "")

        match = re.search(r"https?://(?:www\.)?([^/]+)", link)

        if match:
            return match.group(1)

    return None


def generate_email(domain: str):
    """
    Generate likely company contact emails.
    """

    possible_emails = [
        f"security@{domain}",
        f"contact@{domain}",
        f"info@{domain}",
        f"hello@{domain}"
    ]

    return possible_emails


def run(company: str):
    """
    Find a likely contact email for a company.
    """

    domain = extract_domain(company)

    if not domain:
        return {
            "company": company,
            "email": None
        }

    emails = generate_email(domain)

    return {
        "company": company,
        "domain": domain,
        "email": emails[0]
    }