# Agentic Bug Router & Dispatcher

A multi-agent bug triage pipeline built with **LangGraph**, **Groq**, **Retrieval-Augmented Generation (RAG)**, and the **Model Context Protocol (MCP)**. The system classifies software bug reports, retrieves relevant fixes from a local knowledge base, drafts incident emails, and dispatches them automatically to the appropriate engineering team.

---

## Features

- Multi-agent workflow using LangGraph
- LLM-based bug classification and routing
- Local semantic search using Sentence Transformers
- Offline runbook retrieval with similarity search
- Automated email dispatch via Gmail using MCP

---

## System Architecture

```text
             Bug Report
                  │
                  ▼
      Classification Agent
                  │
                  ▼
        Semantic RAG Search
                  │
                  ▼
        Email Drafting Agent
                  │
                  ▼
     MCP Execution (Gmail API)
                  │
                  ▼
       Engineering Team Inbox
```

---

## 🤖 Agents

### 1. Classification & Routing Agent

Powered by **Llama-3.3-70B-Versatile**.

Task:

- Analyze incoming bug reports
- Determine the responsible engineering team
- Generate a concise technical summary


### 2. RAG Retrieval Agent

A fully offline semantic search component that searches the local knowledge base (`runbooks.txt`).

Uses:

- `sentence-transformers`
- `all-MiniLM-L6-v2`
- NumPy cosine similarity

Task:

- Embed the bug summary
- Search for similar historical incidents
- Retrieve the most relevant solution
- Reject low-confidence matches using a similarity threshold

No external API calls are required for retrieval.

---

### 3. Email Drafting Agent

Generates a professional incident email using:

- Bug summary
- Assigned department
- Retrieved runbook solution

The generated email is formatted for quick review and dispatch.

---

### 4. Execution Agent

Uses the **Model Context Protocol (MCP)** to communicate with a local Node.js Gmail server.

Task:

- Connect to Gmail
- Send the generated incident email
- Notify the appropriate engineering team automatically

---


## Project Structure

```text
.
├── main.py
├── agents.py
├── state.py
├── mcp_client.py
├── runbooks.txt
├── requirements.txt
├── .env
├── gcp-oauth.keys.json
└── README.md
```

---

## Requirements

- Python 3.10+
- Node.js
- npm / npx
- Groq API Key
- Google Cloud OAuth Desktop Credentials

---

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### Create a virtual environment

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 📧 Gmail MCP Setup

Place your Google OAuth credentials in the project root:

```text
gcp-oauth.keys.json
```

Authenticate Gmail once:

```bash
npx @gongrzhe/server-gmail-autoauth-mcp auth
```

A browser window will open requesting Gmail authorization.

---

## Usage

Run the application:

```bash
python3 main.py
```

Enter any software bug report when prompted.

Example:

```text
Hey, the new login page is throwing a 401 Unauthorized error right after I put in my password.
```

The workflow will automatically:

1. Classify the bug report
2. Identify the responsible engineering team
3. Search the local runbook for a relevant fix
4. Draft an incident email
5. Send the email through Gmail

---

##  Sample Queries

### Frontend

```text
The button is overlapping the text on mobile.
```

### Database

```text
Users are getting a 500 Internal Server Error while saving profiles.
```

### Authentication

```text
SAML SSO login is failing for enterprise clients.
```

### Backend

```text
Payment API randomly returns a 502 Bad Gateway response.
```

---

##  How RAG Works

1. The bug report is summarized by the routing agent.
2. The summary is embedded using **all-MiniLM-L6-v2**.
3. Runbook entries are embedded using the same model.
4. Cosine similarity identifies the closest matching incident.
5. The best matching solution is returned if it exceeds the similarity threshold.
The retrieval system uses `runbooks.txt` as its knowledge base.
Adding historical incidents and their resolutions improves the quality of retrieved solutions without requiring additional API calls.

---

## PS: Customizations

The project is designed to be easily adapted for different organizations. Most customizations only require changes in three files.

### `agents.py`

Update the routing logic to match your organization.

Things you may want to customize:

- Team names (e.g., `Frontend`, `Database`, `Authentication`)
- Department email addresses
- Routing prompt used by the classification agent
- Email signature used by the drafting agent

---

### `runbooks.txt`

This file serves as the local knowledge base for the RAG pipeline.

To improve retrieval quality:

- Replace the sample incidents with your own historical bugs and fixes.
- Keep the same format:

```text
[Backend]

Issue:
Users receive a 500 error while saving profiles.

Fix:
Restart the PostgreSQL connection pool.
```

> **Note:** Section headers should match the routing categories defined in `agents.py`.

---

### `main.py`

Only minor customization is typically required.

For example, you can change the terminal banner:

```text
=== Agentic Bug Router & Dispatcher ===
```

to your organization's preferred application name.

---

##  Workflow

This project demonstrates how a multi-agent workflow can automate that process by combining LLM-based routing, semantic retrieval, and tool execution through MCP.

```text
Bug Report
      ↓
Classification
      ↓
Knowledge Retrieval
      ↓
Email Drafting
      ↓
Autonomous Email Dispatch
```

---
