# The workflow, end to end

pstack moves through six phases. Each phase has a skill or a playbook that does the work, and each phase leaves evidence the next one builds on. On OpenCode you load a skill with the `skill` tool and its exact ID, and you run the playbooks through `/poteto-mode`. This page condenses the lifecycle and points at the source of truth for every step.

The [principles](./principles.md) page names the standards that hold across all six phases. The [verification](./verification.md) page covers the proof step in depth.

## 1. Understand

Read before you write. Editing code you do not understand is how subtle regressions ship. An agent that starts editing without a traced model fixes the symptom at the first plausible spot.

- [`how`](../../skills/how/SKILL.md) traces runtime mechanics. It answers at the level of a senior engineer onboarding you, with the runtime flow, the key types, and the non-obvious parts. For a wide subsystem it fans out read-only explorers first.
- [`why`](../../skills/why/SKILL.md) digs up history. It starts from source control, then queries every evidence category your MCPs expose in parallel: issue tracker, long-form docs, team chat, observability, error tracking, and analytics. The report cites its sources and separates evidence from inference.
- [`teach`](../../skills/teach/SKILL.md) blends both into one plain explanation when a summary is not enough. It runs `how` and `why` and weaves the findings together. "Convince me" is the framing worth stealing.
- [`recall`](../../skills/recall/SKILL.md) rebuilds your own recent context on a topic. On OpenCode it reads session history with `opencode session export`, not a Claude transcript path.

Ask the question you actually have. `why` then `how` is a good order when you suspect the history explains the mess.

## 2. Design

One attempt at a hard design locks in the first shape the model thought of. Settle types and boundaries before implementation.

- [`architect`](../../skills/architect/SKILL.md) grounds itself first with `how` and `why`, then runs an arena of competing design sketches. Each sketch writes the caller's usage first, then types, signatures, and a module map. It proceeds into implementation by default. Say "with checkpoint" to review the design first.
- [`arena`](../../skills/arena/SKILL.md) is the tool underneath. N subagents attempt the same brief in parallel, a read-only judge scores them, and the coordinator picks a base and grafts the best parts from the losers.
- [`swarm`](../../skills/swarm/SKILL.md) covers slices and races. Each worker owns one scope and one check, then reports `PASS`, `ISSUES`, or `BLOCKED`. The parent returns one report. Reach for it when parallelism buys coverage, not when you are comparing designs.
- [`interrogate`](../../skills/interrogate/SKILL.md) sends the same diff to reviewers on different model families. A finding two models raise independently is high-confidence signal. It sorts findings into `Act on`, `Consider`, `Noted`, and `Dismissed`, and applies nothing on its own.
- The [prototype playbook](../../skills/poteto-mode/playbooks/prototype.md) is planning with code. Build throwaway variants behind one switcher, drive them, and let the observation decide. The prototype is a throwaway instrument and the real build follows the Feature playbook.

Measure twice, cut once. Most changes need none of this. A small change you are unsure about needs `interrogate` alone. A change that crosses a function boundary earns `architect`, which brings `arena` with it.

### Working backwards

For shared code and packages other people will use, write the usage or the readme first. Start by describing the API to a hypothetical user, then derive the types and signatures from that description, and work back to the implementation. This puts on the developer experience hat before a single line of code locks in a shape.

Use [`technical-writing`](../../skills/technical-writing/SKILL.md) for the readme. It applies the Diátaxis framework to separate the four modes: a tutorial teaches by doing, a how-to guide solves one real problem for an experienced user, reference is the dry complete description of the machinery, and explanation clarifies background, design choices, and tradeoffs. One document that tries to be all four reads badly. Split it.

Readme-driven development also gives the agent a concrete target to check its work against, and it makes the plan easy for you to read.

## 3. Build and clean

The build playbooks share one discipline. Say what you observed, and let the playbook demand the evidence.

- The [Bug fix](../../skills/poteto-mode/playbooks/bug-fix.md) playbook states the symptom and asks for a reproduction first.
- The [Feature](../../skills/poteto-mode/playbooks/feature.md) playbook states the behavior and what must not change.
- The [Refactoring](../../skills/poteto-mode/playbooks/refactoring.md) playbook pins behavior before structure moves.
- The [Perf issue](../../skills/poteto-mode/playbooks/perf-issue.md) playbook states the measurement, not a vibe.
- The [Hillclimb](../../skills/poteto-mode/playbooks/hillclimb.md) playbook drives one number up with one hypothesis at a time and a frozen measurement harness.

[`tdd`](../../skills/tdd/SKILL.md) writes the smallest test that fails for the intended reason, then the fix, then reruns the test. If a test needs broad harness setup or brittle mocks, it says so and uses the closest executable check instead. Do not force a test where a real command is stronger evidence.

Clean before you commit. [`deslop`](../../skills/deslop/SKILL.md) removes code slop and narration from the diff. [`unslop`](../../skills/unslop/SKILL.md) removes AI tells from prose, including the PR description and commit bodies. [`no-comments`](../../skills/no-comments/SKILL.md) hands the comments to a reviewer who did not write them and offers to encode each claimed constraint as a type, test, or lint.

[`correct`](../../skills/correct/SKILL.md) is the lesson step. When the operator corrects the same mistake twice, it turns that mistake class into structure at the highest level that works. Architecture first, then types, then a lint whose error names the fix, then a test, and docs last. Each new check is proven against a real past mistake, and the rule table lives in `AGENTS.md`.

## 4. Verify and ship

"It compiles" is not evidence. State the finish condition up front, then check the real artifact. The [verification](./verification.md) page covers the full proof step, the project verification skill, and the feature map.

- [`create-verification-skill`](../../skills/create-verification-skill/SKILL.md) gives the agent a scripted way to drive your app. On OpenCode it writes to `.opencode/skills/`, OpenCode's project skill directory, with `.claude/skills/` and `.agents/skills/` also resolving. [`maintain-verification-skill`](../../skills/maintain-verification-skill/SKILL.md) keeps the skill and its feature map honest.
- The [Opening a PR playbook](../../skills/poteto-mode/playbooks/opening-a-pr.md) works from a worktree, rebases the work into small ordered commits, cleans the diff, unslops the prose, and returns the PR link. Small ordered commits beat one fat one.
- [`babysit`](../../skills/babysit/SKILL.md) and the [Babysit playbook](../../skills/poteto-mode/playbooks/babysit.md) drive an open PR to merge-ready. They take blockers in order: conflicts, then review threads, then CI. Babysit stops at merge-ready and never merges.
- The [Shipping playbook](../../skills/poteto-mode/playbooks/shipping.md) verifies each PR independently before it arms anything. The agent that judges a change is never the one that wrote it. It lands only the contiguous verified run from the bottom.

## 5. Overnight and larger programs

An agent you trust to verify its own work is an agent you can leave alone with a hard task. What makes that safe is a checkable finish condition, an isolated worktree, and a decision log you audit in the morning.

The [Autonomous run playbook](../../skills/poteto-mode/playbooks/autonomous-run.md) holds the loop: check the finish condition, make the smallest justified change, verify against the real artifact, commit on progress, and log one decision row. On OpenCode there is no built-in loop skill. Re-check manually.

- [`figure-it-out`](../../skills/figure-it-out/SKILL.md) designs the run's phases before any code and wires in the decision log. A duration is not a finish condition, so give the run a predicate that can pass or fail.
- [`show-me-your-work`](../../skills/show-me-your-work/SKILL.md) is what makes the run reviewable. Each row records the time, phase, decision, reason, an evidence pointer, and the result. It stays local by default and commits when a reviewer needs the trail.
- The [Orchestrate playbook](../../skills/poteto-mode/playbooks/orchestrate.md) runs a program that outlives any single agent. The coordinator authors briefs and keeps the lowest unmerged PR green, and never writes code itself.
- The [Autopilot-full playbook](../../skills/poteto-mode/playbooks/autopilot-full.md) runs a queue of independent PRs to merged. No owner merges on its own verdict.
- The [Autopilot-stack playbook](../../skills/poteto-mode/playbooks/autopilot-stack.md) runs the same owner loop but ships nothing. You wake to one linear stack and land it yourself.

On OpenCode, subagents run in the background with the `subagent` tool's `background: true` field. A background subagent returns at once and notifies when done.

## 6. Make it yours

poteto-mode is one person's style. The machinery underneath works the same wearing yours.

- [`automate-me`](../../skills/automate-me/SKILL.md) reads your style out of your history, asks which patterns are really you, and drafts `.opencode/skills/<your-name>-mode/SKILL.md`. Run it again when your habits drift, and it mines only the history since the last edit.
- [`reflect`](../../skills/reflect/SKILL.md) captures a session's lessons right after a task that taught you something. Three parallel reviewers propose edits, a synthesizer sorts them, and nothing changes until you approve.
- [`technical-writing`](../../skills/technical-writing/SKILL.md) holds the bar for docs, RFCs, readmes, PR descriptions, and commit messages. Agent-facing prose has a higher bar than human prose, because an unhelpful sentence becomes an instruction a future agent follows.
- The [Authoring or modifying a skill playbook](../../skills/poteto-mode/playbooks/authoring-a-skill.md) validates the frontmatter and links and ships the result through the Opening a PR playbook. Author the `SKILL.md` per the Agent Skills spec and let the playbook hold the bar.
- The [Eval playbook](../../skills/poteto-mode/playbooks/eval.md) tests a skill change blind. Candidates get an organic-looking task in sanitized directories and never see the words "eval" or "candidate". One judge scores all outputs, and you read every output yourself before accepting the verdict.

Do not edit a skill mid-task because it is misbehaving. Fix it in its own PR and keep the task moving.
