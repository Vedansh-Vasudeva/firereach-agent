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
    if not req.company:
        return {
            "status": "error",
            "message": "A target company is required for the FireReach prototype.",
        }

    if not req.email:
        return {
            "status": "error",
            "message": "A recipient email is required to complete automated outreach.",
        }

    result = run_agent(
        {
            "icp": req.icp,
            "task": req.task,
            "company": req.company,
            "email": req.email,
        }
    )

    return {
        "status": result.get("status"),
        "message": result.get("message"),
        "data": result.get("result"),
    }
