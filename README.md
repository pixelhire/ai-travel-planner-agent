# Autonomous Research Agent

An AI agent that autonomously researches a topic using web search, content extraction, summarization, and persistent memory to generate structured research reports.

---

## Architecture

User Query  
↓  
Research Planner  
↓  
Task Decomposition  
↓  
Web Search (DuckDuckGo)  
↓  
Content Extraction (Newspaper3k)  
↓  
Context Summarization (LLM)  
↓  
Vector Memory Storage  
↓  
Knowledge Aggregation  
↓  
Final Research Report

---

## Agent Workflow

Query Input  
↓  
Generate Research Tasks  
↓  
Search Web Sources  
↓  
Extract Article Content  
↓  
Summarize Key Information  
↓  
Store Knowledge in Vector Memory  
↓  
Aggregate Research Notes  
↓  
Generate Structured Report

---

## Features

✔ Autonomous research workflow  
✔ Web search integration  
✔ Article content extraction  
✔ LLM-powered summarization  
✔ Persistent vector memory  
✔ Chat history persistence  
✔ Markdown research reports  
✔ Containerized deployment

---

## Tech Stack

Python  
FastAPI  
LangChain  
OpenAI API  
Chroma Vector DB  
DuckDuckGo Search  
Newspaper3k  
Docker  
Vanilla JavaScript UI

---

## Data Persistence

Chat History → JSON storage  
Research Memory → Vector database  
Secrets → Mounted `.secrets` volume

---

## Deployment

Dockerized service with persistent storage and mounted secrets.

Run locally:

```bash
docker compose up --build
```
