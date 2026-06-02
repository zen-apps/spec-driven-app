"""Backend agent core package.

A thin FastAPI wrapper around the LangChain agent from
`examples/create_agent.ipynb`. Module layout (teaching-first — each file is one
clear step in the request path):

    config.py   -> settings (model, project, location, credentials path)
    tools.py    -> the six deterministic teaching tools + demo data constants
    schemas.py  -> AutonomousAgentResponse + API request/response models
    metrics.py  -> message-trace helpers (final answer, tool calls, tokens)
    agent.py    -> LLM + create_agent wiring + run_agent() helper
    main.py     -> FastAPI app + POST /chat
"""
