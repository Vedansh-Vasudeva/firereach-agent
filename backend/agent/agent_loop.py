from backend.services.llm_service import call_llm
from backend.agent.tool_registry import TOOLS
from backend.agent.prompts import SYSTEM_PROMPT

MAX_STEPS = 8
TOOL_SEQUENCE = [
    "tool_signal_harvester",
    "tool_research_analyst",
    "tool_outreach_automated_sender",
]


def run_agent(user_input: dict):
    user_message = f"""
ICP: {user_input.get("icp")}

Task: {user_input.get("task")}

Company: {user_input.get("company")}
Email: {user_input.get("email")}
"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    step = 0
    last_result = {}

    while step < MAX_STEPS:
        expected_tool = TOOL_SEQUENCE[step] if step < len(TOOL_SEQUENCE) else None

        response = call_llm(messages)

        if "tool_name" not in response:
            if step >= len(TOOL_SEQUENCE):
                return {
                    "status": "completed",
                    "result": last_result,
                }
            return {
                "status": "error",
                "message": "Agent stopped before completing the required 3-tool sequence.",
            }

        tool_name = response["tool_name"]
        tool_args = response.get("arguments", {})

        if tool_name != expected_tool:
            return {
                "status": "error",
                "message": f"Expected {expected_tool}, but agent selected {tool_name}.",
            }

        if tool_name not in TOOLS:
            return {"status": "error", "message": f"Unknown tool: {tool_name}"}

        if tool_name == "tool_signal_harvester":
            tool_args = {"company": user_input.get("company")}
        elif tool_name == "tool_research_analyst":
            tool_args = {
                "company": user_input.get("company"),
                "icp": user_input.get("icp"),
                "signals": last_result.get("signals", []),
            }
        elif tool_name == "tool_outreach_automated_sender":
            tool_args = {
                "company": user_input.get("company"),
                "email": user_input.get("email"),
                "icp": user_input.get("icp"),
                "signals": last_result.get("signals", []),
                "account_brief": last_result.get("account_brief", ""),
            }

        tool_function = TOOLS[tool_name]
        tool_result = tool_function(**tool_args)

        if tool_name == "tool_signal_harvester":
            last_result = {
                "company": user_input.get("company"),
                "signals": tool_result.get("signals", []),
                "signal_summary": tool_result.get("signal_summary", ""),
                "sources": tool_result.get("sources", []),
            }
        elif tool_name == "tool_research_analyst":
            last_result = {
                **last_result,
                "account_brief": tool_result.get("account_brief", ""),
            }
        else:
            last_result = {
                **last_result,
                "email": tool_result.get("email"),
                "subject": tool_result.get("subject"),
                "body": tool_result.get("body"),
                "html": tool_result.get("html"),
                "delivery_status": tool_result.get("delivery_status"),
            }

        messages.append({
            "role": "assistant",
            "content": f"Tool {tool_name} returned: {tool_result}",
        })

        step += 1

        if step == len(TOOL_SEQUENCE):
            return {
                "status": "completed",
                "result": last_result,
            }

    return {
        "status": "failed",
        "message": "Agent exceeded maximum steps",
    }
