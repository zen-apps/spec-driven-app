# SDD Commands

Each step is now a skill. Run the slash command instead of pasting the full prompt.
`>` lines are manual actions you do at the keyboard (commits, merges, context clears).
`/clear` lines mean: clear the agent's context before the next command.

## Prerequisites — set these up before running any skill

Keep them simple `.md` files at the repo root.

- **`AGENTS.md`** — *required.* The front door every agent reads: project name (`# Project`),
  tech stack, commands, branch naming conventions, and deployment. The skills read this for the
  project identity and branch rules, so it must exist.
- **`README.md`** — *optional but recommended.* Any non-technical context to orient the agent —
  goals, background, voice transcriptions, anything you want to dump in.
- **`TODO.md`** — *optional but recommended.* The disposable inbox for raw, unvetted ideas.
  `sdd-roadmap-from-todo` triages it into the roadmap; `sdd-validation-todo` writes findings back
  into it. Without it, the roadmap comes purely from the constitution interview.

> The constitution skills will still run without `README.md` / `TODO.md`, but they produce a
> better roadmap when both exist.

---

## One time per project

```
/sdd-constitution-greenfield     # new project, from scratch
/sdd-constitution-brownfield     # existing codebase
```

> Review the git diff of mission.md / tech-stack.md / roadmap.md. Request changes through the agent, don't hand-edit.

---

## Per feature cycle — always start here

```
/clear
/sdd-roadmap-from-todo           # triage TODO.md into roadmap.md (no branch)
```

> Review the staged roadmap changes, then commit + open a PR (see AGENTS.md `## Commits` / `## PRs` — yes, PR even for roadmap-only updates on the stable branch).

```
/clear
/sdd-feature-spec                # next phase → branch + plan/requirements/validation
```

> Review plan.md / requirements.md / validation.md before implementing, then commit the spec.

```
/sdd-implement-feature           # build the plan, mark the phase complete
```

> Review the staged changes per task group, run/test the app locally, then commit each group with the proposed message. Commit the staged roadmap update.
> If small tweaks needed, ask the agent to update; otherwise revise the plan and re-run.

---

## Independent validation — SEPARATE agent session

> Open a different agent session (ideally a different CLI), not just `/clear`.
> The validator's independence depends on running outside the implementer's context.

```
/sdd-independent-validator       # code vs validation.md → validation-report.md
```

```
/sdd-validation-todo             # report → triaged TODO.md (feeds back to roadmap-from-todo)
```

> Answer the `→ DECISION:` lines in TODO.md before promoting anything to the roadmap.

---

## After a feature ships

```
/clear
/sdd-replan                      # reconcile constitution after the feature
```

> Commit the staged replan changes, push the branch, open a PR into the stable branch named in AGENTS.md `## Branch Strategy`, merge.

```
/sdd-changelog                   # archive completed phases out of roadmap.md
```

> Commit.

---

## Before the next cycle (or stopping)

```
/clear
/sdd-preflight                   # gate: unfinished work? branch merged? next item right? context clear?
```

> Resolve anything preflight flags before starting the next feature.

---

## Skill order at a glance

```
constitution (greenfield | brownfield)   ← once per project
        │
        ▼
  /clear → sdd-roadmap-from-todo          ┐
  /clear → sdd-feature-spec               │ per-feature
           sdd-implement-feature          │ build loop
        │                                 ┘
        ▼  (separate session)
  sdd-independent-validator               ┐ validation pair
  sdd-validation-todo  ──┐                ┘ (loops back to roadmap-from-todo)
        │                │
        ▼                └──► TODO.md ──► back to sdd-roadmap-from-todo
  /clear → sdd-replan                     ┐
           sdd-changelog                  │ between cycles
  /clear → sdd-preflight                  ┘
```

> Note: `/sdd-independent-validator` resolves from the skill's frontmatter `name:` field.
> Make sure that field matches the folder name, or the command won't fire.
