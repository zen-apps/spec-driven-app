# Tool Demo Report

## Goal

The app already demonstrates the full loop: Streamlit chat -> FastAPI -> LangChain agent -> Gemini -> structured response and diagnostics. The weak spot for a classroom demo is that several tools are currently placeholders, so the agent can call them but the tool outputs do not create much visible value.

The recommended direction is to keep the app stateless and simple, but give the tools a small local knowledge world to operate on. That makes tool calling feel more agentic without adding real infrastructure, API keys, databases, or fragile network dependencies.

## Current State

The backend exposes six tools in `backend/app/tools.py`:

- `weather(location)` has two deterministic locations and is already useful for conditional tool-calling demos.
- `web_search(query)` has one deterministic response for `"latest on ai"`.
- `validate_answer(answer, evidence)` performs a minimal evidence check.
- `run_sql(query)` only echoes the query.
- `search_docs(query)` always reports no internal documents.
- `save_artifact(content)` simulates persistence by returning content length.

The frontend already surfaces tool use well through Agent Diagnostics, including tools triggered, iterations, token usage, confidence, findings, and limitations. That means the best improvement is not a UI change. It is better demo data and better deterministic tool behavior.

## Recommendation

Create a small, readable demo fixture layer and upgrade the existing tools to use it. Do not introduce new frameworks or services.

Recommended fixture shape:

```text
backend/app/demo_data/
├── knowledge_base.md
├── sales.csv
└── artifacts/
```

Suggested roles:

- `knowledge_base.md`: a short markdown file with class-friendly content about SDD, the app architecture, Docker ports, credentials setup, and a few "company policy" facts.
- `sales.csv`: a tiny tabular dataset with 10-20 rows for SQL-style questions.
- `artifacts/`: optional local output directory for saved summaries if you want `save_artifact` to write a real file later. If avoiding writes during the demo is preferable, keep `save_artifact` simulated.

This keeps the demo grounded in visible files students can open, while still showing the agent choosing tools, reading external context, validating an answer, and optionally saving a result.

## Proposed Tool Upgrades

### 1. Make `search_docs` search a local markdown file

Keep it simple: read `knowledge_base.md`, split by headings, score sections by keyword overlap, and return the top 2-3 snippets with headings.

Why this works well in class:

- Students can inspect the exact source file.
- The agent can cite internal context instead of guessing.
- No vector database is needed.
- It demonstrates the shape of RAG without teaching embeddings yet.

Example prompt:

```text
Use the internal docs to explain how this project runs locally and what each service does. Then validate your answer.
```

Expected tool chain:

```text
search_docs -> validate_answer
```

### 2. Make `run_sql` execute safe queries against a tiny local dataset

Use Python standard library only. Either:

- Load `sales.csv` into an in-memory `sqlite3` database on each call, then allow read-only `SELECT` queries.
- Or skip SQL parsing and expose a narrower `query_sales(metric, region)` style tool. This is simpler, but less impressive for the current `run_sql(query)` name.

Recommended guardrails:

- Only allow queries whose first SQL keyword is `SELECT`.
- Reject `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `ATTACH`, and multiple statements.
- Limit returned rows to a small number.
- Return a readable table-like string.

Example prompt:

```text
Use SQL to find the top product by revenue, then validate the answer against the query result.
```

Expected tool chain:

```text
run_sql -> validate_answer
```

### 3. Make `web_search` a curated fake search index

Instead of one hard-coded `"latest on ai"` branch, define a small dictionary of demo search results. Return title, date, source, and summary for a few known queries.

Suggested topics:

- `"latest on ai"`
- `"langchain tools"`
- `"streamlit fastapi demo"`
- `"spec driven development"`

Why this works:

- It looks like a real search result without needing live web access.
- It is deterministic for tests and demos.
- It creates enough content for the agent to synthesize findings.

Example prompt:

```text
Search the web for the latest on AI, compare it with the internal SDD docs, and recommend one thing students should try next.
```

Expected tool chain:

```text
web_search -> search_docs -> validate_answer
```

### 4. Keep `weather`, but add one or two demo cities

The current `weather` tool is already good for conditional planning. Add a few more deterministic locations so prompts are less brittle.

Suggested entries:

- `Delano`: foggy, 60 F
- `New York`: sunny, 75 F
- `Minneapolis`: cloudy, 48 F
- `Phoenix`: hot, 98 F

Example prompt:

```text
If it is hotter than 50 degrees in Delano, search the web for latest on AI. Otherwise, explain why no search was needed.
```

Expected tool chain:

```text
weather -> web_search
```

### 5. Make `save_artifact` return a named artifact receipt

The current function accepts only `content` and returns length. For demo clarity, consider changing it later to:

```python
save_artifact(name: str, content: str) -> str
```

It can still be simulated, but the output should look like a real receipt:

```text
Artifact saved: ai-summary.md
Characters: 842
Preview: ...
```

If you want a little more substance, write to `backend/app/demo_data/artifacts/` during local runs. That would make the demo tangible, but it does introduce filesystem writes inside the container, so simulated save is the safer classroom default.

Example prompt:

```text
Search internal docs for the project architecture, write a short student handout, validate it, and save it as architecture-handout.md.
```

Expected tool chain:

```text
search_docs -> validate_answer -> save_artifact
```

## Suggested Demo Data

### `knowledge_base.md`

Include 5-7 short sections:

- Project mission: teach Spec-Driven Development.
- Architecture: Streamlit frontend, FastAPI backend, LangChain agent, Gemini model.
- Local run flow: credentials, Docker Compose, frontend on 8501, backend host port 8001.
- SDD workflow: constitution, roadmap, feature specs, validation.
- Tool policy: tools are deterministic classroom examples, not production integrations.
- Troubleshooting: missing credentials, backend not reachable, checking container logs.

### `sales.csv`

Use a tiny dataset like:

```text
date,region,product,units,revenue
2026-05-01,North,Notebook,14,210
2026-05-02,South,Marker Set,9,135
2026-05-03,West,Desk Lamp,4,320
...
```

Keep it small enough that students can understand it at a glance.

## Implementation Path

1. Add `backend/app/demo_data/knowledge_base.md` and `backend/app/demo_data/sales.csv`.
2. Upgrade `search_docs` to read and keyword-search the markdown sections.
3. Upgrade `run_sql` to use standard-library `sqlite3` over `sales.csv` with read-only protections.
4. Expand `web_search` from one conditional branch into a small curated search index.
5. Add 2-3 locations to `weather`.
6. Optionally update `save_artifact` to accept `name` plus `content`, or keep the current signature if avoiding API-contract changes matters more.
7. Add focused pytest coverage for the upgraded tools:
   - `search_docs` returns relevant snippets.
   - `run_sql` accepts `SELECT` and rejects writes.
   - `web_search` returns curated results for known topics.
   - `weather` returns deterministic demo locations.
8. Add a short "Demo Prompts" section to `README.md` after the tools are upgraded.

## Recommended First Slice

For the smallest high-impact change, do only this first:

1. Add `knowledge_base.md`.
2. Make `search_docs` search it.
3. Expand `web_search` to 3-4 curated results.
4. Add two polished demo prompts to `README.md`.

That gives the chatbot a stronger tool story without touching the frontend, Docker setup, dependency list, or agent architecture.

## Classroom Demo Prompts

Use these once the tools are upgraded:

```text
Use the internal docs to explain the purpose of this repo and how the app is wired together. Validate your answer before responding.
```

```text
If it is hotter than 50 degrees in Delano, search the web for latest on AI and connect the result to the SDD lesson.
```

```text
Use SQL to find the top product by revenue in the demo sales data. Then explain the answer and validate it against the query result.
```

```text
Create a short student handout about running this app locally. Use internal docs, validate the result, and save the artifact.
```

## Risks and Tradeoffs

- Avoid live external APIs for the demo tools. Real APIs are impressive but introduce latency, keys, network failures, and unpredictable outputs.
- Keep the data obviously fake and labeled as demo data. Students should understand the agent framework pattern, not mistake the fixtures for production integrations.
- Be careful changing tool signatures. Existing tests and prompts assume current names, and `save_artifact` currently accepts only `content`.
- Do not add persistence unless it is part of a later roadmap phase. The current stateless design is a useful teaching constraint.

## Bottom Line

The best "sweeten the pot" move is a deterministic local tool playground: one searchable markdown knowledge base, one tiny queryable dataset, and a curated fake web index. It will make the agent visibly plan, call multiple tools, compare evidence, and return structured diagnostics while keeping the code easy enough to explain in class.
