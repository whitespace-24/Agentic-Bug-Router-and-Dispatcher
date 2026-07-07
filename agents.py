from langchain_groq import ChatGroq
from state import AgentState
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")
print("[System] Loading SentenceTransformer (all-MiniLM-L6-v2)...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

#cosine similarity like assignment 2
def compute_cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def categorize_bug(state: AgentState):
    print("\n[Agent 1] Supervisor analyzing bug report...")
    prompt = f"""
    Categorize this bug report: "{state['raw_bug']}"
    
    Categories and Emails:
    1. Frontend (Email: 24b0946@iitb.ac.in)
    2. Database (Email: 24b0946@iitb.ac.in)
    3. Authentication (Email: 24b0946@iitb.ac.in)
    4. Unclassified (Email: 24b0946@iitb.ac.in)
    
    Format response EXACTLY like this:
    CATEGORY: [Category]
    EMAIL: [Email]
    SUMMARY: [1-sentence summary]
    """
    response = llm.invoke(prompt).content.strip().split('\n')
    
    category = response[0].replace("CATEGORY:", "").strip()
    email = response[1].replace("EMAIL:", "").strip()
    summary = response[2].replace("SUMMARY:", "").strip()
    
    print(f" -> Routed to: {category} Team")
    return {"category": category, "dev_email": email, "summary": summary}

def retrieve_runbook(state: AgentState):
    print(f"[Agent 2] RAG Retriever performing semantic search on runbooks...")
    
    try:
        with open("runbooks.txt", "r") as f:
            content = f.read()
    except FileNotFoundError:
        return {"runbook_solution": "No runbook file found."}

    # Parse the runbook text
    issues = []
    fixes = []
    for line in content.split('\n'):
        if line.startswith('Issue: '):
            issues.append(line.replace('Issue: ', '').strip())
        elif line.startswith('Fix: '):
            fixes.append(line.replace('Fix: ', '').strip())

    if not issues:
        return {"runbook_solution": "No valid issues found in runbook."}

    # Embed the runbook issues & the user's bug summary
    issue_embeddings = embedder.encode(issues)
    query_embedding = embedder.encode(state['summary'])

    # Calculate  Cosine Similarity
    best_score = -1
    best_idx = -1
    
    for i, doc_emb in enumerate(issue_embeddings):
        score = compute_cosine_similarity(query_embedding, doc_emb)
        if score > best_score:
            best_score = score
            best_idx = i

    # Threshold check > 0.4
    if best_score > 0.4:
        solution = fixes[best_idx]
        print(f" -> Semantic Match Found (Score: {best_score:.2f}): {solution}")
    else:
        solution = "No known fix in runbooks. Manual investigation required."
        print(f" -> No strong semantic match (Best Score: {best_score:.2f}). Hallucination guard activated.")

    return {"runbook_solution": solution}

def draft_ticket(state: AgentState):
    print("[Agent 3] Drafting emergency dispatch email with RAG context...")
    prompt = f"""
    Write a short, urgent email to the {state['category']} team.
    
    Issue Summary: {state['summary']}
    Original Report: {state['raw_bug']}
    Suggested Fix (from Runbooks): {state['runbook_solution']}
    
    Requirements:
    - Address the {state['category']} team.
    - Include the Suggested Fix so the developer knows exactly what to do.
    - Keep it under 5 sentences.
    - Sign off as: Automated Dispatch System
    
    Write ONLY the email body.
    """
    response = llm.invoke(prompt)
    return {"draft": response.content.strip()}
