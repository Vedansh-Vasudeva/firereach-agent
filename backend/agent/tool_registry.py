from backend.tools.company_discovery import run as company_discovery
from backend.tools.signal_harvester import run as signal_harvester
from backend.tools.research_analyst import run as research_analyst
from backend.tools.contact_finder import run as contact_finder
from backend.tools.outreach_sender import run as outreach_sender


TOOLS = {
    "company_discovery": company_discovery,
    "signal_harvester": signal_harvester,
    "research_analyst": research_analyst,
    "contact_finder": contact_finder,
    "outreach_sender": outreach_sender
}