import requests
from backend.config import config

SERP_API_URL = "https://serpapi.com/search"


def search_google(query, num_results=5):
    """
    Uses SerpAPI to perform a Google search.

    Returns top organic results.
    """
    if not config.SERPAPI_KEY:
        return []

    params = {
        "q": query,
        "api_key": config.SERPAPI_KEY,
        "engine": "google",
        "num": num_results
    }

    response = requests.get(SERP_API_URL, params=params, timeout=20)

    if response.status_code != 200:
        return []

    data = response.json()

    results = []

    for item in data.get("organic_results", []):
        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        })

    return results
