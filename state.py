from typing import TypedDict

class AgentState(TypedDict):
    raw_bug: str
    category: str
    dev_email: str
    summary: str
    runbook_solution: str  # New RAG context
    draft: str