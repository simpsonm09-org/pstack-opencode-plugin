# Prompts and pitfalls

Prompts worth copying, then the mistakes everyone makes once. Swap in your own paths and finish conditions. The recipes stay informal, since that is how they get typed and the skills read intent fine.

Every skill below is loaded with the `skill` tool and its exact ID. On OpenCode that ID is the folder name under `skills/`. A skill named in a prompt, such as `how` or `swarm`, is a real skill in this plugin. The plugin injects the routing instruction through a session context hook, which tells the agent to load `poteto-mode` for work that touches more than one file, changes a shared signature, involves a design choice, or has an unknown bug cause. A workspace `AGENTS.md` can carry its own instructions alongside it.

## In your own words

The indirect prompt asks the agent to restate the problem before it starts. Instead of telling the agent exactly what to do, you draw the understanding out of the agent in its own words.

This is a human prompting technique. It is not agent behavior, and no skill performs it for you.

Use it when someone reports an issue and you want a shared reading of the problem before any code is written. The example prompt reads a thread and states the issue back.

```text
Load poteto-mode. Read this thread and restate in your own words and in plain English what you think the underlying issue is. Do not change anything yet.
```

Three reasons this works.

- It forces the agent to compress a noisy conversation into a structured problem statement. A long thread with several guesses collapses into one sentence you can check.
- It lets you catch a misunderstanding early. If the agent fixates on a red herring, you correct it before it writes any code.
- You have not led it down the wrong path with your own assumptions. Stating your hypothesis first can be wrong, and it can limit what the agent finds on its own.

The same idea shows up in `teach`, which explains a body of work plainly and runs `how` and `why` underneath. Use `teach` when you want to understand what the agent did and why it makes sense, not just to read its summary.

## Copy-paste recipes

Each recipe is a prompt block and one line of setup. Replace the bracketed parts with real paths and commands. `prove it works` names the `principle-prove-it-works` standard, which requires evidence from the real artifact.

### Understand a subsystem

Mechanics first, history second. Each skill's report names the sources it searched, so you know what the answer rests on.

```text
Load poteto-mode. Use how first to understand how this initialization works. Then use why to figure out why it broke recently.
```

### Get a second opinion on a design

Your current design becomes one candidate among several. The synthesis tells you whether the panel found something better or confirmed what you had.

```text
Load poteto-mode. Ask arena for a second opinion on this thread and our approach.
```

### Check independent slices in parallel

Each worker owns one slice. The parent waits for every slice and returns one `PASS`, `ISSUES`, or `BLOCKED` report instead of raw worker dumps.

```text
Load poteto-mode. Use swarm to check every package under packages/ against its check script. One worker per package. One report.
```

### Review a branch skeptically

The qualifiers do real work. "Do not change anything yet" keeps the review read-only, and the nitpick rule pre-filters the noise so the act-on findings are worth your time.

```text
Load poteto-mode. Interrogate the whole branch, but skeptically. Do not change anything yet. No nitpicks unless it is an actual bug or a regression in behavior.
```

### Fix a bug through a failing test

The "if there is a cheap test path" clause matters. Forcing a test through brittle mocks proves less than running the real command, and `tdd` is allowed to say the cheap path does not exist.

```text
Load poteto-mode. Reproduce the duplicate write first and show the failing run. If there is a cheap test path, use tdd. Then find the root cause, fix it, and rerun. Prove it works on the real surface.
```

### Verify a change

Three prompts for showing the work instead of claiming it. Each one asks for evidence from the running app.

```text
Load poteto-mode. Build the feature, then drive it the way a user does with the project verify skill. Show me screenshots and a transcript of the run as proof.
```

```text
Load poteto-mode. Take a baseline trace with the project verify skill, make one targeted fix, then take another trace. Show me the measured delta.
```

```text
Load poteto-mode. Reproduce the reported symptom on the real app first. Show me the failing run before you touch anything.
```

### Keep a run honest while you are away

The short form works once the task and the finish condition are already in the conversation. `show-me-your-work` keeps the decision trail you audit later. For a long overnight run, use `figure-it-out`, which designs the playbook for a large or multi-part effort.

```text
I am going to bed. Keep going autonomously until every fixture passes. Do not stop. Keep a decision log I can audit in the morning.
```

### Redirect a drifting run

Steering prompts are one line. You rarely need more words. You need the right name, and the [principles](./principles.md) page is the vocabulary.

```text
I said the goal is to reproduce. I did not ask for a fix yet.
```

```text
Apply prove it works. Show me the real output, not the build log.
```

```text
Use unslop on that reply. No em dashes.
```

### Get the reply in plain words

That is the whole prompt.

```text
bro
```

`bro` restates the last message like one human talking to another, with no jargon and shorter. Use it when a reply is technically thorough and you still do not know what it said.

## Pitfalls

- **Enumerating skills in the prompt.** A prompt such as "use how, then architect, then arena" reorders steps the playbook already sequences. State the goal and the constraints. Name a skill only to override a default.
- **A vague finish condition.** "Make it better" gives an autonomous run nothing to check. Give a command or artifact that can pass or fail.
- **Parallel agents in one worktree.** They overwrite each other and the diff becomes archaeology. Say "one worktree per attempt" and the isolation is there. Separate sessions with the same prompt can each get a worktree, but they do not run pstack's cross-judge or synthesis steps for you.
- **Using `arena` for coverage.** `arena` repeats one design or code brief, then picks a base and grafts the best parts. `swarm` splits slices or declared race arms and aggregates one report. Coverage is `swarm`.
- **Accepting every review comment.** Bots and humans file real catches and noise in one list. `interrogate` sorts findings into act-on and dismissed buckets with reasons, and you can override either way.
- **Treating `auto` as a model slug.** Do not pass `auto`, `inherit-parent`, or the Claude aliases `opus`, `fable`, and `sonnet` to OpenCode. A role value of `auto` or `inherit-parent` means the subagent inherits the parent session model. Otherwise use a real `provider/model` from `/models`. The `pstack-opencode` skill names those aliases, and `setup-pstack-opencode` covers model setup.
- **Reporting success off a green build.** A build proves it compiles. Ask for the real command, flow, stored value, or profile, and expect the evidence in the reply. This is the `principle-prove-it-works` standard.
- **Writing a `SKILL.md` freehand.** Route it through the authoring path in `poteto-mode` so validation and review happen.

## OpenCode pitfalls

- Do not read Claude Code transcript paths such as `~/.claude/projects/`. OpenCode does not write them. To mine a session, run `opencode session export <session>`, which prints its messages as JSON. A history scan such as `recall` uses this route.
- The `instructions` array in `opencode.json(c)` is accepted but not loaded. Listing a path there changes nothing. Put standing instructions in `AGENTS.md`, which OpenCode reads.
- Write a project verification skill to `.opencode/skills/verify/`, OpenCode's project skill directory. `.claude/skills/` and `.agents/skills/` also resolve, but `.opencode/skills/` is the path to use. `create-verification-skill` generates it.
- OpenCode has no bundled `run` or `loop` skills. Run app checks through a project verification skill and the shell or browser tools. For repeated checks, re-check by hand.

Back to the [guide index](./README.md).
