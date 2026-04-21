from backend.services.serp_service import search_google


SIGNAL_QUERIES = {
    "funding": "{company} funding OR series A OR series B OR series C",
    "hiring": "{company} hiring OR careers OR jobs engineering sales security",
    "leadership": "{company} new CEO OR new CTO OR leadership change",
    "expansion": "{company} expansion OR growth OR new office OR product launch",
    "security_stack": "{company} cybersecurity OR security platform OR security tooling",
}

SIGNAL_PATTERNS = {
    "funding": {
        "label": "Recent funding momentum",
        "keywords": ["funding", "raised", "series a", "series b", "series c", "investment"],
    },
    "hiring": {
        "label": "Active hiring expansion",
        "keywords": ["hiring", "jobs", "careers", "headcount", "recruiting"],
    },
    "leadership": {
        "label": "Leadership change",
        "keywords": ["ceo", "cto", "chief", "leadership", "appointed", "joined"],
    },
    "expansion": {
        "label": "Company expansion",
        "keywords": ["expansion", "growth", "launch", "new office", "scale", "expands"],
    },
    "security_stack": {
        "label": "Security and infrastructure focus",
        "keywords": ["security", "cybersecurity", "compliance", "platform", "infrastructure"],
    },
}


def run(company: str):
    """
    Deterministically harvest live buyer signals for a given company.
    """
    harvested = []
    seen_sources = set()

    for signal_type, query_template in SIGNAL_QUERIES.items():
        query = query_template.format(company=company)
        results = search_google(query, num_results=4)
        pattern = SIGNAL_PATTERNS[signal_type]

        for result in results:
            text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
            if not any(keyword in text for keyword in pattern["keywords"]):
                continue

            source_key = result.get("link")
            if source_key in seen_sources:
                continue

            seen_sources.add(source_key)
            harvested.append(
                {
                    "type": signal_type,
                    "label": pattern["label"],
                    "evidence": result.get("snippet") or result.get("title"),
                    "source": result.get("link"),
                    "title": result.get("title"),
                }
            )

    signals = [
        {
            "type": item["type"],
            "label": item["label"],
            "evidence": item["evidence"],
        }
        for item in harvested
    ]

    summary = ", ".join(sorted({item["label"] for item in harvested})) or "No qualifying external growth signals found."

    return {
        "company": company,
        "signals": signals,
        "signal_summary": summary,
        "sources": harvested,
    }
