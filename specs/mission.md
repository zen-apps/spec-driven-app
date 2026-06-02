# Mission

## Problem

Most developers learn AI coding agents by "vibe coding" — long, ad-hoc chat
sessions that produce code nobody can explain or reproduce. There is no durable
record of *why* the code looks the way it does, so the work drifts and is hard
to teach from.

This project is a small, real, full-stack AI agent app that exists to be built
**from specs first**. It gives a class a concrete, forkable example of an AI
agent — LangChain with tools and structured output, backed by Google Gemini —
that was driven end-to-end by Spec-Driven Development (SDD) rather than vibes.

## Long-term goal

Be a clean, reusable **reference agent app** that students can clone, run, read,
and extend. The agent pattern is intentionally simple and well-documented (see
[`examples/create_agent.ipynb`](../examples/create_agent.ipynb)) so the
implementation never gets in the way of the lesson: how to direct an AI agent to
build software against written specs.

## Who uses it

**Primary audience: students in a class** learning to use AI coding agents
across the whole stack — frontend, backend, and Python. Their primary needs:

- A working example they can stand up themselves and poke at.
- Code simple enough to walk through live, without hidden magic.
- A visible SDD trail (constitution, feature specs, validation, roadmap) that
  shows how each piece of the app traces back to a spec.

## What success looks like

1. **Runs end-to-end.** `docker-compose up` brings up the Streamlit frontend and
   the FastAPI backend, each on its own port. A user can chat with the agent and
   see its tool calls and final structured output.
2. **Specs drove the build.** Every feature traces to a spec — the constitution
   (`mission.md`, `tech-stack.md`, `roadmap.md`) plus per-feature
   `requirements.md`, `plan.md`, and `validation.md`. The SDD paper trail is
   itself a primary deliverable, not an afterthought.

## Non-goals

- Production hardening (auth, scaling, observability beyond basics).
- A real database or arbitrary code execution — tools are deterministic teaching
  stand-ins, as in the example notebook.
- Breadth of features. Depth and clarity beat surface area.
