# Spec-Driven Development Practice Knowledge Base

Source: `examples/demo_data/sdd_practice.md`, a practice transcript for a 20-minute classroom talk by Josh Janzen about Spec-Driven Development.

## Speaker And Teaching Context

Josh Janzen is a leader of data science at Hormel Foods and a Super Data Science alumnus. The talk introduces Spec-Driven Development, or SDD, as a practical way to work with modern AI coding agents such as Codex, Cursor, Claude Code, and similar tools.

The audience is a group learning how to use AI coding agents more deliberately. The goal is not to sell a specific product or framework. The goal is to teach a simple, framework-agnostic workflow that helps developers steer agents, keep context clean, and understand the code that gets produced.

## Core Idea

Spec-Driven Development is a way to steer AI coding agents with durable written specifications instead of relying only on ad hoc prompts. It is part of the broader idea of harness engineering: the developer no longer writes every line of code manually, but still directs the system by defining intent, boundaries, acceptance criteria, and validation steps.

The central shift is:

- Old pattern: prompt the agent, inspect whether the result seems to work, and keep prompting until it looks right.
- SDD pattern: define what should be built in plain-text specs, let the agent implement against those specs, validate the result, and preserve important project context across sessions.

SDD is especially useful as projects grow larger and more complex, because it gives the agent a stable source of truth and reduces drift.

## Why Vibe Coding Breaks Down

Vibe coding can be fun and productive for small experiments. A developer gives the agent a prompt, reviews the result, and iterates quickly. The problem is that larger projects can drift. The agent may lose track of prior decisions, hallucinate requirements, or create code that runs but is hard to explain.

The early speed of vibe coding can disappear when the developer has to do rework, untangle unclear code, or rediscover why earlier choices were made. SDD is a way to keep the speed while adding structure.

## SDD Compared With TDD And Vibe Coding

Vibe coding uses prompts and visual inspection as the main feedback loop. It is fast but can suffer from drift, hallucination, and expensive rework.

Test-Driven Development, or TDD, uses tests as the source of truth. The developer defines expected behavior in tests, then writes code until those tests pass.

Spec-Driven Development uses written specifications as the source of truth. Specs define the mission, tech stack, roadmap, requirements, implementation plan, and validation criteria. The agent can then implement against those files instead of relying on the current chat history alone.

SDD and TDD can work together. Specs describe what should be built and why. Tests help prove whether the implementation behaves correctly.

## Start With Three Questions

Every software project should start by answering three questions:

1. Why are we doing this?
2. What are we building?
3. How will this be used?

In this workflow, those answers become durable markdown files. The agent can help write them by asking clarifying questions. The developer does not need to perfect everything up front, but the project should have enough written direction for the agent to make good decisions.

## The Project Constitution

The project constitution is the long-lived context for the repo. It usually contains three files:

- `specs/mission.md`: explains why the project exists, who it serves, and what success looks like.
- `specs/tech-stack.md`: explains the languages, frameworks, services, dependencies, deployment target, and testing approach.
- `specs/roadmap.md`: explains the ordered phases or features that should be built.

The constitution gives the agent just enough persistent context to understand the project across sessions. It should be updated when major project decisions change.

## Required And Helpful Root Files

`AGENTS.md` is the most important root-level agent file. It acts like a README for AI coding agents. Agents such as Codex, Cursor, and Claude Code can read it at startup to understand project expectations, commands, architecture, and workflow rules.

`TODO.md` is a raw inbox for future work. It can contain one item or many items. Later, the agent can triage those ideas into the roadmap.

`README.md` is the human-facing explanation of the project. It should explain what the repo does and how a person can run or understand it. It can be refined over time as the project becomes clearer.

## Greenfield And Brownfield Projects

A greenfield project is a new project started from scratch. A brownfield project is an existing project that was already built before SDD was introduced.

SDD works for both. Greenfield projects can start with a clean constitution before code exists. Brownfield projects can be onboarded by having the agent inspect the existing repo, summarize reality, and create the constitution from what is already there.

## The Six-Step SDD Workflow

The workflow has six steps. The first step happens mostly once, steps two and three happen repeatedly, and the last three are hygiene steps that keep the system clean.

1. Create the constitution.
2. Create a feature spec.
3. Implement the plan.
4. Replan after major changes.
5. Move completed roadmap items into the changelog.
6. Run independent validation with a second agent when useful.

Most day-to-day development happens in the loop between feature spec and implementation.

## Step 1: Create The Constitution

The constitution captures the project mission, audience, tech stack, and roadmap. It is the foundation the agent can return to when deciding what code to write and what tradeoffs are acceptable.

For a new project, the constitution starts from the user's intended goals. For an existing project, the constitution starts from the files already in the repo.

## Step 2: Create A Feature Spec

A feature spec turns an item from `TODO.md` or `specs/roadmap.md` into a concrete feature plan. The agent asks clarifying questions when requirements are unclear.

Each feature gets its own dated directory under `specs/`, usually containing:

- `requirements.md`: what the feature must do and what decisions were made.
- `plan.md`: the implementation steps the agent should follow.
- `validation.md`: the acceptance criteria and tests or manual checks needed to prove the feature works.

This step is where the developer steers the agent before code is written.

## Step 3: Implement The Plan

After the feature spec is approved, the agent implements the plan. The agent should work through the plan in order, make focused code changes, run relevant tests, and validate the result against `validation.md`.

The developer still reviews the code and runs the app when appropriate. SDD does not remove engineering judgment. It gives the agent a better target and gives the developer a clearer way to inspect the work.

## Step 4: Replan

Replanning updates the constitution after the project changes. For example, if the app switches model providers, changes its LLM framework, or adds a new service, the tech stack and roadmap may need to be adjusted.

The purpose of replanning is to keep the long-lived docs aligned with reality. If the constitution drifts away from the code, the agent loses the value of that persistent context.

## Step 5: Maintain A Changelog

Completed roadmap phases should move out of `specs/roadmap.md` and into `specs/changelog.md`. This keeps the roadmap focused on open and upcoming work while preserving a record of what shipped.

The changelog acts as lightweight memory for past changes. The agent can still refer to it when needed, but the roadmap stays clean and easier to use as active context.

## Step 6: Independent Validation

For higher-risk changes, a second agent can review the completed feature. The validator should inspect the code and `validation.md` without relying on the original implementation plan. That makes the review more independent.

The second agent can produce findings, missing requirements, or suggested fixes. Those findings can then be passed back to the primary implementation agent.

This review loop is optional, but it is useful for important features or when the developer wants an outside check.

## Context Window Discipline

One major benefit of SDD is cleaner context. Long chats can cause AI coding agents to lose focus as the context window fills. The talk refers to a "dumb zone," a commonly used informal term for the point where agent output quality starts to degrade because the context window is too full.

The practical guidance is to keep context small and focused:

- Store durable decisions in markdown files instead of the chat.
- Clear chat context between major steps when possible.
- Let the agent reload only the relevant specs for the current task.
- Keep roadmap and changelog files concise.

The point is not the exact percentage of context usage. The point is that focused context produces better agent behavior.

## Acceptance Criteria

In vibe coding, a feature may feel done when the app runs. In SDD, a feature is done when it satisfies written acceptance criteria.

Acceptance criteria live in the feature's validation document. They should explain how to prove the work is correct, including automated tests, manual checks, expected API responses, UI behavior, or known limitations.

## Role Of Ask-User Questions

Modern coding agents often have an ask-user or clarification tool. In SDD, that tool is useful during specification. The agent can ask about scope, business rules, data models, user workflows, and acceptance criteria before implementation starts.

Good clarification questions prevent the agent from guessing major requirements.

## Why Markdown Works Well

Markdown files are simple, durable, and easy for both humans and agents to read. They work as a lightweight storage system for project intent.

Using markdown avoids adding a database or custom planning tool too early. The project can stay transparent: students can open the files and see exactly what the agent is using as context.

## Framework-Agnostic Approach

There are many SDD-related tools and frameworks, including GitHub Spec Kit, Amazon Kiro, Agent OS, and other agent workflow systems. The teaching approach in this transcript is intentionally framework agnostic.

The important ideas are not tied to one product:

- Create durable specs.
- Keep context clean.
- Implement against an approved plan.
- Validate against written criteria.
- Update the roadmap and changelog as the project evolves.

## Practical Takeaways

Start every project by answering why, what, and how it will be used.

Move from vibe coding toward harness engineering: steer the agent with specs instead of relying only on prompts.

Keep the context window clean by storing decisions in markdown files and clearing chat history between major steps.

Use independent validation when a second opinion would reduce risk.

Remember that SDD may feel slower at the beginning, but it reduces rework and makes AI-assisted projects easier to explain, maintain, and reproduce.
