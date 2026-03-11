from pydantic import BaseModel
from typing import Optional


class AgentRequest(BaseModel):
    """
    Request model for the FireReach agent.
    This represents the input coming from the user or frontend.
    """

    icp: str
    task: str
    company: Optional[str] = None
    email: Optional[str] = None