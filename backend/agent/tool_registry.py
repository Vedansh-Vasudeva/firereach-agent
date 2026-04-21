from backend.tools.signal_harvester import run as tool_signal_harvester
from backend.tools.research_analyst import run as tool_research_analyst
from backend.tools.outreach_sender import run as tool_outreach_automated_sender


TOOLS = {
    "tool_signal_harvester": tool_signal_harvester,
    "tool_research_analyst": tool_research_analyst,
    "tool_outreach_automated_sender": tool_outreach_automated_sender,
}
