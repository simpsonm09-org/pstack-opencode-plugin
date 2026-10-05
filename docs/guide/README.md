# The pstack guide for OpenCode

pstack works best when you stop micromanaging. You state the goal and how you will know it is done, then you let the agent pick the method and show its evidence. The `poteto-mode` skill is the entry point. It matches the task to a playbook, runs the other skills as the steps need them, and proves the result against the real artifact instead of a proxy such as "it compiles". On OpenCode you also load `pstack-opencode`, which translates pstack's Claude tool names to this runtime.

## Quickstart for OpenCode

The plugin is installed into your workspace and loads for sessions rooted there. When it loads it registers the pstack skills and the OpenCode adapter skills through `ctx.skill.transform`, and it injects the routing instruction through a `session.hook("context")` hook. That hook is the OpenCode equivalent of pstack-claude's SessionStart hook, so the routing text reaches the model without a prompt stub.

Start a task by typing `/poteto-mode` or describing the task in plain language. An agent can also load one skill directly with the `skill` tool and the skill's exact ID, for example `poteto-mode`. The injected routing instruction tells the agent to load `poteto-mode` when a task touches more than one file, changes a shared signature, involves a design choice, or has an unknown bug cause. For smaller tasks the agent works directly and verifies on the real artifact.

Models are not configured by the upstream Claude sheet or a Cursor `pstack-models.mdc`. Set a model on an OpenCode agent profile through the workspace model policy instead. The `setup-pstack-opencode` skill owns this and supersedes the upstream sheet's `opencode` row. The `pstack-opencode` skill warns you not to translate the Claude aliases `opus`, `fable`, and `sonnet` into OpenCode IDs. Use a real `provider/model` from `/models`, optionally with a `#variant`.

A project verification skill is written to `.opencode/skills/verify/`. That is OpenCode's project skill directory, and `.claude/skills/` and `.agents/skills/` also resolve. The `create-verification-skill` skill generates it. See [verification.md](./verification.md) for the full page.

## If you only remember one thing

Paste this when a bug needs a fix you can trust.

```text
Load poteto-mode. Here is a bug: <symptom and how to trigger it>.
Reproduce it first and show the failing run, then find the root cause,
then fix it and show the passing run. Verify on the real surface.
```

The point is the order. Reproduce, trace to the root cause, fix, then prove the fix on the same surface.

## Index

- [verification.md](./verification.md) covers a project verification skill under `.opencode/skills/verify/` and how to use it.
- [principles.md](./principles.md) covers the pstack coding standards, the principles the agent must read and cite for the choices it makes.
- [workflows.md](./workflows.md) covers the playbooks, from bug fix and feature to refactoring and PR shipping, and how `poteto-mode` picks one.
- [prompts.md](./prompts.md) covers copy-paste prompts you can hand to the agent for common jobs.

## Further reading

This guide adapts two upstream sources for OpenCode. The pstack guide at <https://github.com/cursor/plugins/tree/main/pstack/docs/guide> and the two part article series by the pstack author ([Part 1](https://x.com/poteto/article/2094457600259842065), [Part 2](https://x.com/poteto/status/2097732320606507506)) cover the same material for Cursor and Claude Code. Read them for the original reasoning, and read here for the OpenCode tooling, model setup, and skill paths that differ.
