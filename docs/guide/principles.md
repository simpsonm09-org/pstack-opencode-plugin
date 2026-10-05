# The coding standards

pstack ships 24 principles as individual skills. `poteto-mode` reads their index at the start of a multi-step task, applies the ones the task triggers, and names each applied principle in its reply along with the decision it changed. You steer with those names. Each name points at a rule the agent has already read, so one short phrase redirects the work more precisely than a paragraph of instructions. On OpenCode you can also load a principle directly with the `skill` tool and its ID.

## Core

These decide how much to build and when to rethink the design.

- **Laziness Protocol** (`principle-laziness-protocol`). Aim for the most result with the least code and complexity. Steering: `bias to deletion, smallest change`. See [SKILL.md](../../skills/principle-laziness-protocol/SKILL.md).
- **Foundational Thinking** (`principle-foundational-thinking`). Get the data shape right before writing logic, and choose structures that match the dominant paths. Steering: `data structures first`. See [SKILL.md](../../skills/principle-foundational-thinking/SKILL.md).
- **Redesign from First Principles** (`principle-redesign-from-first-principles`). Integrate a change as if the requirement had been there from the start, instead of bolting it on. Steering: `redesign as if it was always required`. See [SKILL.md](../../skills/principle-redesign-from-first-principles/SKILL.md).
- **Attack the Premise** (`principle-attack-the-premise`). When fixes sharing an assumption fail the same gate, write down what they assumed and choose an observation that can challenge it before another fix depends on it. Steering: `challenge the assumption behind the fixes`. See [SKILL.md](../../skills/principle-attack-the-premise/SKILL.md).
- **Subtract Before You Add** (`principle-subtract-before-you-add`). Remove complexity first, then build on the simpler base. Steering: `remove dead weight first`. See [SKILL.md](../../skills/principle-subtract-before-you-add/SKILL.md).
- **Minimize Reader Load** (`principle-minimize-reader-load`). Track the layers between question and answer and the hidden state a reader must hold, then collapse one-caller wrappers and shrink mutable scope. Steering: `flatten the trace path`. See [SKILL.md](../../skills/principle-minimize-reader-load/SKILL.md).
- **Outcome-Oriented Execution** (`principle-outcome-oriented-execution`). Optimize for the intended end state rather than preserving smooth intermediate states with throwaway compatibility code. Steering: `converge on the target design`. See [SKILL.md](../../skills/principle-outcome-oriented-execution/SKILL.md).
- **Experience First** (`principle-experience-first`). When implementation convenience conflicts with user delight, choose delight. Steering: `ship less, ship better`. See [SKILL.md](../../skills/principle-experience-first/SKILL.md).
- **Exhaust the Design Space** (`principle-exhaust-the-design-space`). When the right answer is not obvious, build 2-3 competing prototypes and compare them side by side before committing. Steering: `show me three options`. See [SKILL.md](../../skills/principle-exhaust-the-design-space/SKILL.md).
- **Build the Lever** (`principle-build-the-lever`). When the work is not trivial, build the tool that does it or proves it instead of doing it by hand. Steering: `build the script, not the manual edits`. See [SKILL.md](../../skills/principle-build-the-lever/SKILL.md).

## Architecture

These decide where state, validation, and compatibility live.

- **Model the Domain** (`principle-model-the-domain`). Encode the real domain in a data structure instead of scattering it across conditionals. Steering: `one structure, not scattered branches`. See [SKILL.md](../../skills/principle-model-the-domain/SKILL.md).
- **Boundary Discipline** (`principle-boundary-discipline`). Place validation, type narrowing, and error handling at system boundaries, trust internal code, and keep business logic in pure functions. Steering: `guard the boundary, trust the core`. See [SKILL.md](../../skills/principle-boundary-discipline/SKILL.md).
- **Type System Discipline** (`principle-type-system-discipline`). Use the type checker to eliminate impossible states, mismatched primitives, and unhandled variants at compile time. Steering: `make illegal states unrepresentable`. See [SKILL.md](../../skills/principle-type-system-discipline/SKILL.md).
- **Make Operations Idempotent** (`principle-make-operations-idempotent`). Design operations so they converge to the correct state regardless of how many times they run or where they start from. Steering: `converge on rerun and crash`. See [SKILL.md](../../skills/principle-make-operations-idempotent/SKILL.md).
- **Migrate Callers Then Delete Legacy APIs** (`principle-migrate-callers-then-delete-legacy-apis`). When the new API is the right design, migrate callers and remove the old API in the same refactor wave. Steering: `migrate and delete in one wave`. See [SKILL.md](../../skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md).
- **Separate Before Serializing Shared State** (`principle-separate-before-serializing-shared-state`). When actors might share mutable state, first check whether they need the same object and eliminate the sharing, and enforce serialization structurally only when sharing is real. Steering: `remove the sharing before adding a lock`. See [SKILL.md](../../skills/principle-separate-before-serializing-shared-state/SKILL.md).

## Verification

These define what counts as proof.

- **Prove It Works** (`principle-prove-it-works`). Verify every task output by checking the real thing directly, not a proxy, a self-report, or "it compiles". Steering: `run the real artifact`. See [SKILL.md](../../skills/principle-prove-it-works/SKILL.md).
- **Fix Root Causes** (`principle-fix-root-causes`). Trace every problem to its root cause and fix it there instead of fixing symptoms. Steering: `trace it to the cause`. See [SKILL.md](../../skills/principle-fix-root-causes/SKILL.md).
- **Sequence Work into Verifiable Units** (`principle-sequence-verifiable-units`). Order work as small units, each ending in a state you can check, and do not advance until the current one is green. Steering: `one green unit at a time`. See [SKILL.md](../../skills/principle-sequence-verifiable-units/SKILL.md).
- **Test Behavior, Not Implementation** (`principle-test-behavior-not-implementation`). Before keeping a test, name a relevant defect and check that the complete test arrangement detects it, and assert the required result or effect including absence when the contract requires it. Steering: `assert the behavior, prove it fails`. See [SKILL.md](../../skills/principle-test-behavior-not-implementation/SKILL.md).
- **Explain the Number** (`principle-explain-the-number`). Before you trust, report, or act on a measured number, find what limits it and rule out that it measured something else. Steering: `explain the number before trusting it`. See [SKILL.md](../../skills/principle-explain-the-number/SKILL.md).

## Delegation

These keep parallel work sane.

- **Guard the Context Window** (`principle-guard-the-context-window`). Keep every token worth its cost by routing bulk to subagents and keeping summaries in the main thread. Steering: `send the bulk to a subagent`. See [SKILL.md](../../skills/principle-guard-the-context-window/SKILL.md).
- **Never Block on the Human** (`principle-never-block-on-the-human`). Make reasonable decisions on reversible work, proceed, and let the human course-correct after the fact. Steering: `proceed, present the result`. See [SKILL.md](../../skills/principle-never-block-on-the-human/SKILL.md).

## Meta

- **Encode Lessons in Structure** (`principle-encode-lessons-in-structure`). Encode recurring fixes in mechanisms such as tools, code, metadata, or automation instead of textual instructions. Steering: `turn the advice into a check`. See [SKILL.md](../../skills/principle-encode-lessons-in-structure/SKILL.md).

## Steering in practice

Say the agent is about to bolt a new adapter onto three existing ones:

```text
use subtract before you add. delete the obsolete adapters first, then design what's left.
```

Say it claims success because the build passed:

```text
apply prove it works. run the real import flow and show me the written records.
```

Say two parallel attempts are about to write to the same branch:

```text
separate before serializing shared state. give each attempt its own worktree, no locks.
```

Each phrase lands because the rule behind it is specific. The agent still has to say which decision the rule changed. A principle citation with no decision behind it is the tell that it name-dropped instead of applied.

Do not memorize the list. Skim it now, then come back when you catch the agent doing something a name here would have prevented. That is how the vocabulary sticks.
