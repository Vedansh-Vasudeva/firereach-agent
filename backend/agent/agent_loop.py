from backend.services.llm_service import call_llm
from backend.agent.tool_registry import TOOLS
from backend.agent.prompts import SYSTEM_PROMPT

MAX_STEPS = 8


def run_agent(user_input: str):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    step = 0
    last_result = None

    while step < MAX_STEPS:

        response = call_llm(messages)

        # If LLM stops calling tools, return last tool result
        if "tool_name" not in response:
            return {
                "status": "completed",
                "result": last_result
            }

        tool_name = response["tool_name"]
        tool_args = response.get("arguments", {})

        if tool_name not in TOOLS:
            return {"status": "error", "message": f"Unknown tool: {tool_name}"}

        print(f"Step {step+1}: Running tool -> {tool_name}")

        tool_function = TOOLS[tool_name]

        tool_result = tool_function(**tool_args)

        # store the latest result
        last_result = tool_result

        # send tool output back to LLM
        messages.append({
            "role": "assistant",
            "content": f"Tool {tool_name} returned: {tool_result}"
        })

        step += 1

    return {
        "status": "failed",
        "message": "Agent exceeded maximum steps"
    }