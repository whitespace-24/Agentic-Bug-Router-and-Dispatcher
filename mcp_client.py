from langchain_mcp_adapters.client import MultiServerMCPClient

def get_mcp_client():
    return MultiServerMCPClient(
        {
            "gmail": {
                "command": "npx",
                "args": ["@gongrzhe/server-gmail-autoauth-mcp"],
                "transport": "stdio",
            }
        }
    )