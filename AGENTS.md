# Project

This repository contains a new software project. The project purpose, target users, and implementation details will be refined as the codebase develops.

Before making major changes, review the project files and ask clarifying questions when requirements are unclear.

## Tech Stack

Update this section as the project is defined.

* Language: Python
* Frontend: Streamlit
* Backend: FastAPI + LangChain
* Database: None (stateless)
* LLM / AI tools: Google Gemini (gemini-3.5-flash via langchain-google-genai)
* Deployment: Docker Compose (local development)
* Package manager: pip (requirements.txt)
* Testing framework: pytest

## Repository Structure

Update this section as directories are added.

```text
.
├── README.md
├── AGENTS.md
├── TODO.md
└── specs/
```

## Commands

Update these commands once the project has runnable code.

```bash
# Install dependencies
pip install -r backend/requirements.txt -r frontend/requirements.txt

# Run the app locally
make build && make up # or docker-compose up

# Run tests
make test-local # or pytest backend/tests

# Run linting / formatting
# TODO
```

## Development Workflow

This repo uses a lightweight Spec-Driven Development workflow.

Long-lived project context should live in:

```text
specs/
├── mission.md
├── tech-stack.md
└── roadmap.md
```

Feature-specific work should live in:

```text
specs/YYYY-MM-DD-feature-name/
├── requirements.md
├── plan.md
└── validation.md
```

## Agent Instructions

When working in this repo:

1. Read `README.md`, `AGENTS.md`, and relevant files in `specs/` before making changes.
2. Do not guess major requirements. Ask clarifying questions when scope, business rules, data models, or acceptance criteria are unclear.
3. Keep changes small, focused, and aligned to the current roadmap item.
4. Prefer updating existing files over creating unnecessary new files.
5. Do not introduce new frameworks, services, or dependencies without explaining why.
6. When implementing a feature, follow the approved `plan.md` and validate against `validation.md`.
7. After completing work, summarize what changed, what was tested, and any remaining risks.

## Branch Strategy

Use clear branch names.

```text
feature/<short-feature-name>
fix/<short-fix-name>
chore/<short-task-name>
docs/<short-doc-change>
```

## Commits

The user handles ALL commits unless explicitly asked otherwise.

When asked to commit, use concise commit messages:

```text
Add initial project constitution
Implement user authentication flow
Fix data validation error
Update roadmap after completed feature
```

## PRs 

Always done by the user, even for roadmap updates on main.

## Testing Expectations

Before considering work complete:

1. Run the relevant test command if available.
2. If tests do not exist yet, explain what should be tested manually.
3. Do not claim something is fully validated unless it was actually tested.

## Safety and Boundaries

Do not modify secrets, credentials, production configuration, or deployment files unless specifically instructed.

Do not delete user work without confirmation.
