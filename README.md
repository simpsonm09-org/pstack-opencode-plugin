# pstack-opencode

An OpenCode plugin that brings PStack into OpenCode. This repository is the source of truth for the plugin package.

When it loads it does two things:

- Registers the pinned PStack skills and the OpenCode adapter skills through `ctx.skill.transform`.
- Injects the PStack routing instruction through a `session.hook("context")` hook, the OpenCode equivalent of pstack-claude's Claude Code SessionStart hook.

## What it does not do

- It cannot create agent profiles. OpenCode's `AgentEditor` has no `add`. The profiles ship in `agents/` and are installed into `.opencode/agents` by the workspace installer.
- It cannot set the workspace model. That stays in the workspace `opencode.jsonc`, and the per-role models come from `maxstack/models.json`.
- Transform-registered skills get a base directory but no `<skill_files>` sample. PStack skills name their own supporting files, so the agent still finds them.

## Guide

The plugin ships an OpenCode-adapted guide under `docs/guide/`. Start at [docs/README.md](docs/README.md), the documentation index. It links the guide pages and the repository root docs, and covers the 24 coding standards, verification, the workflow, and prompts. The guide pages live in `docs/guide/`.

## Upstream sources of truth

PStack starts at the Cursor plugin [cursor/plugins/pstack](https://github.com/cursor/plugins/blob/main/pstack/README.md), is ported to Claude Code at [michael-denyer/pstack-claude](https://github.com/michael-denyer/pstack-claude), and is adapted to OpenCode here. The chain is cursor/plugins pstack to pstack-claude to this repository. The current pin is `michael-denyer/pstack-claude` `8d3aa571` (version 0.9.73), absorbing `cursor/plugins` `2cbf585` and PStack v0.15.13.

`pstack.lock.json` is the single source of the pinned upstream repository and commit. Its `portOf` object records the Cursor repository, the `pstack` path, and the latest absorbed Cursor commit. The Cursor original is the authority for fidelity.

Vendored skills under `skills/` are byte-identical to their source after LF normalization, which is the pinned upstream commit, the port-authored adapter skills under `adapter/skills/`, or the vendor source. The substitutions are declared in [CHANGES.md](CHANGES.md). No substitution currently edits a vendored body. [PORTING.md](PORTING.md) states the policy and the update workflow, and `scripts/upstream-status.py` reports upstream drift.

## Layout

- `index.ts`, `package.json` are the plugin entrypoint and manifest.
- `agents/` holds the hand-authored OpenCode agent profiles: `pstack-agent`, `pstack-reviewer`, `pstack-comment-sicko`. Model lines are injected by the workspace installer from `maxstack/models.json`; keep no `model:` line here.
- `adapter/skills/` holds the hand-authored adapter skills `pstack-opencode`, `setup-pstack-opencode`, and `port-pstack`.
- `vendor/skills/` is the carry slot for upstream content ahead of the pin, mirrored into `skills/` by the build. It is currently empty, and the mechanism remains for a future carry. It is upstream-sourced, not port-authored.
- `adapter/AGENTS.md` is the historical global routing instruction, kept for reference.
- `skills/` is generated. Do not hand-edit it.
- `scripts/build.ps1` regenerates `skills/` from the pinned upstream, the adapter sources, and `vendor/skills/`.
- `scripts/verify-pin.py` checks the generated tree against the pin, the adapter sources, and `vendor/skills/`.
- `scripts/upstream-status.py` reports upstream drift against the pin.
- `pstack.lock.json` pins the upstream `pstack-claude` repository and commit, plus the Cursor `portOf` source.
- `PORTING.md` states the faithful-port policy and the update workflow. `CHANGES.md` declares the substitutions.
- `docs/guide/` is the port-authored guide, adapted for OpenCode.

## Build

The pinned upstream clone lives at `%LOCALAPPDATA%\maxstack\pstack-claude`.

```powershell
pwsh -File scripts/build.ps1
python3 scripts/verify-pin.py --clone "$env:LOCALAPPDATA\maxstack\pstack-claude"
```

`NOTICE`, `LICENSE`, `LICENSE-cursor-team-kit`, and `NOTICE-port.md` carry the upstream attribution and are refreshed by the build.

## Install

`maxstack` consumes this repository. Its `Install-Workspace.ps1` copies the package into `.opencode/plugins/pstack-opencode` in the workspace and runs `npm install` there, because the plugin needs `@opencode/plugin` in its own `node_modules`.

Do not run `opencode plugin add` for this package unless global activation is intended. The plugin is active only for sessions under the workspace that installs it.

## Workspace pin

The workspace pins this repository by commit. `stack.lock.json` in the workspace root and `pstack-opencode.lock.json` in `maxstack` both record the SHA the installer copies into `.opencode/plugins/pstack-opencode`. The package publishes `pstack.lock.json`, `scripts/`, `adapter/`, and `vendor/skills/` in its `files` list, so a consumer can rebuild `skills/` from the same upstream commit with the package alone.

`pstack.lock.json` is the single source of the upstream `repository` and `commit`. `scripts/build.ps1` reads both to regenerate `skills/`, and `verify-pin.yml` plus `scripts/verify-pin.py` read both to prove the generated tree matches the pin and the adapter sources. The check fails on any drift.

## CI

`.github/workflows/verify-pin.yml` reads `pstack.lock.json`, clones that repository at that commit, and runs the pin check on push and pull request. Run the same checks locally:

```bash
mise install
mise run lint
python3 scripts/verify-pin.py --clone <pinned-clone>
```

## License

This plugin is a port of upstream MIT work. The port stays MIT.

- The vendored skills come from [`cursor/plugins/pstack`](https://github.com/cursor/plugins/tree/main/pstack) and [`cursor/plugins/cursor-team-kit`](https://github.com/cursor/plugins/tree/main/cursor-team-kit), through the Claude Code port [`michael-denyer/pstack-claude`](https://github.com/michael-denyer/pstack-claude).
- Upstream copyright is Lauren Tan (pstack) and Cursor (cursor-team-kit), both MIT. Their notices and license texts travel beside this file in [`LICENSE`](LICENSE), `LICENSE-cursor-team-kit`, `NOTICE`, and `NOTICE-port.md`.
- The port-authored OpenCode adapter code is MIT, `Copyright (c) 2026 simpsonm09`, in [`LICENSE-port`](LICENSE-port).

`scripts/build.ps1` regenerates `LICENSE`, `LICENSE-cursor-team-kit`, `NOTICE`, and `NOTICE-port.md` from the pinned upstream. Do not hand-edit them.
