# Spec-Driven App

A simple demo app for teaching **Spec-Driven Development (SDD)** — how to use
AI coding agents to build software from clear specs instead of vibes.

## What we're building

A small AI agent app, split into separate services that each run in their own
Docker container:

- **Backend** (`./backend`) — a Python **FastAPI** app that wraps a
  **LangChain** agent. The agent uses **structured output** and **tools**, with
  **Google Gemini** as the LLM.
- **Frontend** (`./frontend`) — a **Streamlit** UI that talks to the backend.
- **docker-compose** — spins up both services, each on its own port.

The agent pattern we're copying lives in
[`examples/create_agent.ipynb`](examples/create_agent.ipynb).

## Why

This is a teaching project. The goal is to show a class how to drive a real
build with AI agents across the whole stack — **frontend, backend, and
Python** — by writing specs first and letting the agent implement against them.

## Layout

```text
.
├── backend/         # FastAPI + LangChain agent (Python)
├── frontend/        # Streamlit UI
├── examples/        # reference notebooks (agent + RAG)
├── credentials/     # Gemini LLM credentials (gitignored)
├── specs/           # spec-driven development docs
└── docker-compose.yml
```

