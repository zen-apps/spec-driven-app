# Mission

## Problem

Most developers build software from "vibes" — improvising with AI coding agents
without a durable plan. The result is inconsistent output, lost context between
sessions, and code that nobody can explain or reproduce. There is no clear,
end-to-end example showing how to drive a real full-stack build with AI agents
by writing specs *first* and letting the agent implement against them.

## Long-term goal

Teach **Spec-Driven Development (SDD)**: a workflow where a project is anchored
by a constitution (mission, tech stack, roadmap) and each feature is built from
a written spec before any code. This repo is the teaching vehicle — a small but
real AI agent app — that lets a class watch the whole SDD loop play out across
the frontend, backend, and Python layers.

The app being built is intentionally modest: a LangChain agent (structured
output + tools, powered by Google Gemini) wrapped in a FastAPI backend, with a
Streamlit frontend, each service in its own Docker container and wired together
with docker-compose. The app matters less than the *process* used to build it.

## Who uses it

**Developers learning SDD** — working developers, typically in a class setting,
who already write code but want to learn how to drive AI coding agents with
specs instead of ad-hoc prompting.

Their primary needs:

- A clear, followable example of the SDD workflow from empty repo to running app.
- To see *why* each piece of code exists, traceable back to a spec.
- A pattern they can carry into their own projects.

## What success looks like

A **working demo app**: the backend and frontend both come up via
`docker-compose`, and the agent answers requests end to end — using its tools
and returning structured output through the Streamlit UI.

Because this is a teaching project, success also implies the path there is
legible: each phase of the build was driven by a spec, so the class can trace
the running app back to the documents that produced it.
