Agentic SaaS Bug Router & Dispatcher

An enterprise-grade, multi-agent automated triage system built with LangGraph, Groq, and the Model Context Protocol (MCP). This system ingests unstructured bug reports, categorizes them, performs semantic vector searches against a local runbook to find known solutions, and autonomously dispatches formatted alert emails to the relevant engineering teams.

🏗️ Architecture

This project utilizes a Supervisor/Worker multi-agent workflow:

The Supervisor Agent (Router): Analyzes the raw bug report using llama-3.3-70b-versatile to determine the specific engineering department (Frontend, Database, Auth, etc.) and extracts a concise technical summary.

The RAG Retriever (Semantic Search): A fully local agent operating completely offline. It uses sentence-transformers (all-MiniLM-L6-v2) and manual NumPy cosine similarity to embed the bug summary and search runbooks.txt for known company fixes. Includes a hallucination guard threshold.

The Drafter Agent: Synthesizes the extracted summary and the RAG-retrieved solution into a highly urgent, professional dispatch email.

The Execution Agent (MCP): Uses the Model Context Protocol to interface with the Gmail API via a local Node.js server, autonomously dispatching the drafted email to the targeted department.

🚀 Features

Multi-Agent Orchestration: Strict separation of concerns via LangGraph state dictionaries.

Local Semantic RAG: Zero-token vector search for extracting internal knowledge base fixes.

Tool Use & Execution: Native MCP integration for real-world API interactions.

Modular Design: Cleanly separated states, prompts, and execution logic.

🛠️ Prerequisites

Python 3.10+

Node.js & npx (for the MCP server)

A Groq API Key

Google Cloud OAuth Client ID (Desktop App) for Gmail API access

⚙️ Setup & Installation

Clone the repository:

git clone <your_repo_url>
cd <your_repo_directory>


Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate


(Note: If you run this on Windows, the activation command is venv\Scripts\activate)

Install dependencies:

pip install -r requirements.txt


Environment Variables:
Create a .env file in the root directory and add your Groq key:

GROQ_API_KEY=your_groq_api_key_here


MCP Credentials:
Place your Google Cloud OAuth JSON file in the root directory and rename it exactly to gcp-oauth.keys.json.

Authenticate the MCP Server:
Run the following command to generate your local Gmail token before running the main script. Follow the browser prompt to log in and allow access:

npx @gongrzhe/server-gmail-autoauth-mcp auth


💻 Usage

Run the main orchestrator:

python3 main.py


You will be prompted to enter a software bug complaint. The agents will take over, process the text, find the runbook solution, and send the email automatically.

Example Input:

"Hey, the new login page is throwing a 401 Unauthorized error right after I put in my password."
