# Plan — Backend: full LangChain agent endpoint (Phase 2)

Each task group is independently implementable and verifiable. The plan proceeds logically from environment and dependencies to helpers, tools, agent creation, and finally endpoint implementation.

## 1. Environment & Container Setup (`docker-compose.yml`, requirements)

1. Update `backend/requirements.txt` to include:
   - `langchain==1.3.0`
   - `langchain-community==0.4.1`
   - `langchain-google-genai==4.2.4`
   - `pydantic>=2.0` (FastAPI compatible)
2. Update `./docker-compose.yml` to mount the `./credentials` directory to the backend container under `/app/credentials` and set environment variables:
   ```yaml
   services:
     backend:
       ...
       volumes:
         - ./credentials:/app/credentials:ro
       environment:
         - GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/credentials.json
         - GEMINI_PROJECT=${GEMINI_PROJECT:-zen-general-377713}
         - GEMINI_LOCATION=${GEMINI_LOCATION:-global}
   ```

## 2. Models & Helper Utilities (`backend/app/helpers.py`)

1. Define `AutonomousAgentResponse(BaseModel)` as specified in the requirements.
2. Port the content normalization helpers from the notebook:
   - `normalize_content(content: Any) -> str`
   - `get_final_answer_from_messages(result: dict) -> str`
   - `get_structured_response(result: dict) -> Optional[AutonomousAgentResponse]`
   - `get_final_answer(result: dict) -> str`
3. Port the metric summarization helper:
   - `summarize_agent_metrics(result: dict) -> dict` which counts tool-calls, logs sequences, and aggregates token usages.

## 3. Demo Placeholder Tools (`backend/app/tools.py`)

1. Define the `@tool` decorated functions matching `create_agent.ipynb` exactly:
   - `run_sql(query: str) -> str`
   - `validate_answer(answer: str, criteria: str) -> str`
   - `search_docs(query: str) -> str`
   - `save_artifact(name: str, content: str) -> str`
   - `weather(location: str) -> str`
   - `web_search(query: str) -> str`

## 4. Agent Assembly & Initialization (`backend/app/agent.py`)

1. Initialize `ChatGoogleGenerativeAI`:
   - Read `GEMINI_PROJECT` and `GEMINI_LOCATION` from environment variables, defaulting to `"zen-general-377713"` and `"global"`.
   - Instantiate with model `"gemini-3.5-flash"` and `temperature=1.0`.
2. Construct the agent using `create_agent`:
   - Supply the model, list of 6 tools, `AutonomousAgentResponse` response format, and the system prompt.
3. Expose a single runner function `run_agent(prompt: str) -> dict` which:
   - Invokes `agent.invoke` with the input message and `recursion_limit: 50`.
   - Returns the raw dictionary result.

## 5. API Endpoint Integration (`backend/app/main.py`)

1. Define a Pydantic input schema `ChatRequest` containing a single `message: str` field.
2. Implement the `POST /chat` endpoint:
   - Accept `ChatRequest`.
   - Call `run_agent` with the message.
   - Extract the structured `AutonomousAgentResponse` using helper utilities.
   - Generate metrics JSON via `summarize_agent_metrics`.
   - Return combined success dictionary containing `"response"` and `"metrics"`.
3. Implement `try-except` block to catch downstream exceptions (e.g. Google API errors, auth failures):
   - Catch all exceptions.
   - Print/log the exception details.
   - Return a `500 Internal Server Error` with `detail` and a populated fallback `response` and empty `metrics` block matching the planned schema.

## 6. Verification & Validation

1. Run `docker-compose build` to verify the backend container compiles successfully with the new packages.
2. Run `docker-compose up` to launch the stack.
3. Fire a verification `POST /chat` request using `curl` and observe success metrics or detailed failure fallbacks.
