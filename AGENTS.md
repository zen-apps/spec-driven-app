# Project Context for AI Agents

This project follows a spec-driven development workflow. Before doing any work,
read the project constitution in `specs/`.

## Constitution (read these first, in order)

- `specs/mission.md` — Why this project exists, who it serves, scope and non-goals.
- `specs/tech-stack.md` — Technical decisions, languages, libraries, deployment.
- `specs/roadmap.md` — Phased plan. Check this before suggesting next steps.

## Per-feature specs

Each feature is developed on its own branch with three files in `specs/<feature-name>/`:

- `plan.md` — How the feature will be built, step by step.
- `requirements.md` — What must be true for the feature to be considered done.
- `validation.md` — How we will verify it works.

When implementing a feature, read all three before making changes.

## Ideas inbox

`TODO.md` is a scratchpad for uncommitted ideas — things to consider for future
roadmap phases. It is **not** authoritative. The roadmap in `specs/roadmap.md` is
the source of truth for what to build next. During replanning, items from TODO.md
may be promoted to roadmap phases; once promoted, they are removed from TODO.md.

Do not treat TODO.md items as work to be done unless I explicitly ask.

## Working agreements

- Never modify files in `specs/` without an explicit instruction.
- When implementing a feature, keep changes scoped to that feature's branch.
- If a request conflicts with the constitution, raise it before proceeding.
- Prefer asking a clarifying question over guessing.

## Tooling

- Use the `feature-spec` skill when starting a new feature.
- Use the `changelog` skill before merging a feature branch to main.