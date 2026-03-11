import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Central configuration class for API keys and project settings.
    """

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")

    MAX_AGENT_STEPS = 8


config = Config()