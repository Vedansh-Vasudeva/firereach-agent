import json
import re
from groq import Groq
from backend.config import config

client = Groq(api_key=config.GROQ_API_KEY)


def call_llm(messages, model="llama-3.3-70b-versatile", temperature=0.2):

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