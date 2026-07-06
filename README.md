# Agentic-Bug-Router-and-Dispatcher
A multi-agent automated triage system built with LangGraph, Groq, and the Model Context Protocol (MCP). This system ingests unstructured bug reports, categorizes them, performs semantic vector searches against a local runbook to find known solutions, and autonomously dispatches formatted alert emails to the relevant engineering teams.

## Architecture

This project utilizes a Supervisor/Worker multi-agent workflow:

1. **The Supervisor Agent (Router):** Analyzes the raw bug report using `llama-3.3-70b-versatile` to determine the specific engineering department (Frontend, Database, Auth, etc.) and extracts a concise technical summary.
2. **The RAG Retriever (Semantic Search):** A fully local agent operating completely offline. It uses `sentence-transformers` (`all-MiniLM-L6-v2`) and manual NumPy cosine similarity to embed the bug summary and search `runbooks.txt` for known company fixes. Includes a hallucination guard threshold.
3. **The Drafter Agent:** Synthesizes the extracted summary and the RAG-retrieved solution into a highly urgent, professional dispatch email.
4. **The Execution Agent (MCP):** Uses the Model Context Protocol to interface with the Gmail API via a local Node.js server, autonomously dispatching the drafted email to the targeted department.

## Features
* **Multi-Agent Orchestration:** Strict separation of concerns via LangGraph state dictionaries.
* **Local Semantic RAG:** Zero-token vector search for extracting internal knowledge base fixes.
* **Tool Use & Execution:** Native MCP integration for real-world API interactions.
* **Modular Design:** Cleanly separated states, prompts, and execution logic.

## Requirements
* Python 3.10+
* Node.js & `npx` (for the MCP server)
* A Groq API Key
* Google Cloud OAuth Client ID (Desktop App) for Gmail API access

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <your_repo_url>
   cd <your_repo_directory>
