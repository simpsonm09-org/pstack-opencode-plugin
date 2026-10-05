# Verification is the foundation

A verification skill lets an agent check its own work. The agent runs the app, drives the feature the way a user would, and captures proof that the change works. When it can do that, it closes the loop on its own and you stop being the bottleneck. A verification skill lets people who do not read the code confirm that a change works.

pstack treats verification as infrastructure, not as one skill among many.

## Create one

Run the `create-verification-skill` skill. It interviews the repo instead of you. It finds the surface a user touches, how the app starts, how an agent can drive it, and what evidence counts as proof. Then it writes a project-local skill.

On OpenCode that skill goes to `.opencode/skills/verify/`. That is OpenCode's project skill directory. `.claude/skills/` and `.agents/skills/` also resolve, but write to `.opencode/skills/` first. At the repo root a project skill named `verify` is the driver every pstack playbook calls, so name it `verify`. In a monorepo, write it in the package you touched.

The generated skill teaches an agent to launch the app, run a read-only doctor check before driving it, drive one mapped feature, capture evidence, and clean up. It writes for the next agent, which reads it cold mid-task and has never seen the app.

Maintain it with the `maintain-verification-skill` skill. A feature map rots the moment the app changes, so the upkeep loop re-reads source per feature, drives every feature live, and ships at most one PR of proven corrections. Run it on a cadence. A recurring OpenChamber scheduled task fits here. The upstream article suggests once a day, and that is a reasonable starting point.

## Make it reproducible

The `principle-build-the-lever` skill says to build the tool instead of doing the work by hand. For verification that means a small CLI that scripts interaction with the app, not a throwaway script per run. A CLI command costs fewer tokens than an agent writing a one-off clicker, and it reruns the same way every time.

Design the CLI for an agent to read and compose.

- Prefer deep commands over a wide flat API.
- Put a `--dry-run` on anything with a destructive side effect.
- Use subcommands so the agent reads one part at a time instead of the whole surface.
- Return machine-readable output, for example JSON.
- Write error messages that name the fix, not just the failure.
- Ship rich `--help` text.

The article groups useful commands into categories. A given app will not need all of them, so pick the ones the surface supports.

- Inspection: `info`, `snapshot`, `screenshot`, `components`
- Navigation: `home`, `new-session`, `select-project`, `select-runtime`, `scroll`
- Interaction: `send`, `click`, `click-xy`, `aria-click`, `type`, `press`, `eval`, `upload-image`, `add-context`, `feature-flag`
- Performance: `trace`, `profile`, `record`, `perf-metrics`, `wait-settle`
- Streaming: `console`, `network-log`, `network-summary`
- Health and cleanup: `doctor`, `cleanup`, `watch --restart`

Also think about the dev experience the CLI sits on. Seeding a dev database, handling auth and test users, pointing API calls at a test or staging environment, and bringing up the environment the same way every time. You already needed this when you wrote the code yourself.

## The feature map

A feature map is a searchable index of the user-facing features in the app. It says what each feature does and how a user reaches it. The generator writes it next to the verification skill as `features/README.md` plus one file per feature. The README is the map. Each feature file is the recipe.

Every feature file uses four H2 sections, in this order.

- `Sub-features` lists short IDs with one line per behavior.
- `How to get to it (user POV)` lists every user entry point.
- `Driving it with <harness>` starts with `Preconditions:` and pairs each user action with an exact command and an observable result.
- `Gotchas` lists traps that waste or invalidate a run.

The example generator output is under `skills/create-verification-skill/references/feature-map-example/`. Read the README there for the index and conventions, then `create-note.md` and `search.md` for two worked feature files.

The map saves tokens. It gives the agent the exact entry points and commands for a feature instead of making it rediscover them from source on every task. Treat it as shared memory that everyone contributing to the repo benefits from, and keep it current with `maintain-verification-skill`.

## Parallelism

The article recommends Cursor cloud agents, which run on Cursor's infrastructure with their own machine. OpenCode has no cloud agent feature, so do not expect one. The equivalents here are local.

- Run work as `subagent` calls with `background: true`. A background subagent returns at once and notifies when it finishes, so you can keep other work moving.
- Give each writer its own git worktree or branch. Two agents writing the same checkout clobber each other.
- Use an OpenChamber scheduled task for a recurring run, for example the daily `maintain-verification-skill` pass. A repository with no commit has no worktree base, so fall back to owning the change directly.

## How to use it with prompts

Copy-paste recipes for building a feature, measuring performance, and reproducing a report live in `./prompts.md`.
