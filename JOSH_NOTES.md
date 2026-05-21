AGENTS.md is the front door every agent reads; the constitution is the structured knowledge behind that door."

TODO.md as inbox. A scratchpad for raw, unvetted ideas. "Add export to Parquet. Look into Polars vs Pandas. User asked about Slack notifications." It's messy on purpose. During replanning, you triage it: items that survive the cut get promoted to the roadmap with proper phasing; items that don't get deleted or moved to a backlog. The roadmap stays clean and ordered; TODO.md stays informal and disposable.

Claude Code CLI
$ ln -s AGENTS.md CLAUDE.md

"You'll see a lot of named frameworks in this space — Spec-Kit, Kiro, BMAD, OpenSpec, Tessl, and more landing every month. They're all packaging the same underlying practice we're going to learn today: write a constitution, spec the feature, plan the work, implement against the plan, validate. We're going to do it in plain Markdown, with no installs and no CLIs, for three reasons. One, you can apply it tomorrow with whatever agent you already use. Two, when these frameworks evolve — and they're evolving fast — you'll recognize what they're doing and pick the one that fits your workflow. Three, you can't outgrow the fundamentals. Once you've internalized the practice, layering a tool on top is straightforward; trying to learn a tool without the practice underneath is how you get cargo-cult adoption."
That's a thirty-second framing that does three things: positions your choice as deliberate, signals you know the landscape, and reframes "minimal tooling" from a limitation into a feature. It also pre-empts the "but what about Spec-Kit?" question that will otherwise come up at minute 40.
One small tactical add: a closing slide on "where to go next"
At the end of the session, a single slide listing the major frameworks with a one-line note on each:

GitHub Spec-Kit — open-source CLI that automates the workflow you learned today; best for greenfield + larger features
AWS Kiro — productized IDE with built-in spec-driven workflow; best if you live in AWS
BMAD-METHOD — multi-agent (PM/architect/dev personas) for larger team workflows
Cursor Plan Mode / Claude Code Skills — lighter native versions inside the agents you may already use
Tessl, OpenSpec, Augment Code — emerging commercial options