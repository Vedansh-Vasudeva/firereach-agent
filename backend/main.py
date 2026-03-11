from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models.request_models import AgentRequest
from backend.agent.agent_loop import run_agent


app = FastAPI()


# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "FireReach Agent Running"}


@app.post("/run-agent")
def run_agent_endpoint(req: AgentRequest):

    query = f"""
ICP: {req.icp}

Task: {req.task}

Company: {req.company}
Email: {req.email}
"""

    result = run_agent(query)

    return {
        "status": result.get("status"),
        "data": result.get("result")
    }