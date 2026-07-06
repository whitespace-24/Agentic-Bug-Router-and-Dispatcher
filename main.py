import asyncio
import logging
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from state import AgentState
from agents import categorize_bug, retrieve_runbook, draft_ticket
from mcp_client import get_mcp_client

# Suppress the noisy plain-text MCP warning
logging.getLogger("mcp").setLevel(logging.CRITICAL)
load_dotenv()

def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("categorize_bug", categorize_bug)
    builder.add_node("retrieve_runbook", retrieve_runbook)
    builder.add_node("draft_ticket", draft_ticket)

    # The new linear RAG pipeline
    builder.set_entry_point("categorize_bug")
    builder.add_edge("categorize_bug", "retrieve_runbook")
    builder.add_edge("retrieve_runbook", "draft_ticket")
    builder.add_edge("draft_ticket", END)

    return builder.compile()

async def main():
    print("=== Enterprise SaaS Bug Router & RAG Dispatcher ===\n")
    raw_bug = input("Enter a software bug complaint:\n> ")

    initial_state = {
        "raw_bug": raw_bug,
        "category": "",
        "dev_email": "",
        "summary": "",
        "runbook_solution": "",
        "draft": ""
    }

    graph = build_graph()
    result = graph.invoke(initial_state)

    print("\n--- Final Drafted Email ---")
    print(result["draft"])
    print("---------------------------\n")

    print("[Agent 4] Connecting to Gmail MCP to send alert...")
    client = get_mcp_client()
    tools = await client.get_tools()
    
    send_tool = next((tool for tool in tools if "send" in tool.name.lower()), None)
    
    if send_tool:
        try:
            await send_tool.ainvoke({
                "to": [result['dev_email']],
                "subject": f"[BUG ALERT] {result['category']} System Issue",
                "body": result["draft"]
            })
            print(f"[Success] Alert dispatched successfully to {result['dev_email']}!")
        except Exception as e:
            print(f"\n[Error] Failed to send email: {e}")
    else:
        print("\n[Error] No send tool found in MCP server.")

if __name__ == "__main__":
    asyncio.run(main())