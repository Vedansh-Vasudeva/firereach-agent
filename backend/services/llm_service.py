import json
import re
from backend.config import config

try:
    from groq import Groq
except ImportError:
    Groq = None

client = Groq(api_key=config.GROQ_API_KEY) if Groq and config.GROQ_API_KEY else None


def call_llm(messages, model="llama-3.3-70b-versatile", temperature=0.2):
    if not Groq:
        return {"content": "LLM request skipped because the groq package is not installed."}

    if not config.GROQ_API_KEY:
        return {"content": "LLM request skipped because GROQ_API_KEY is not configured."}

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )

    content = response.choices[0].message.content

    # Try direct JSON
    try:
        return json.loads(content)

    except:
        pass

    # Try extracting JSON block from text
    try:
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    # fallback
    return {"content": content}
