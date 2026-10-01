# Cross-platform task runner for humans and agents. `just --list` shows every
# recipe. Keep each recipe a thin call to a portable tool or a script under
# scripts/. See https://github.com/simpsonm09-org/simpsonm09-repo-standard/blob/main/docs/task-runner.md
set windows-shell := ["powershell.exe", "-NoLogo", "-NoProfile", "-Command"]

# List the recipes.
default:
    @just --list

# Install the pinned tools.
install:
    mise install

# Run every linter over the tracked files.
lint:
    mise exec -- flint run --full

# Fix what the linters can fix.
lint-fix:
    mise exec -- flint run --fix

# Run the AI-slop gate.
aislop:
    npx --yes aislop@0.16.1 ci

# Check the vendored skills against the pinned upstream clone.
# Needs the clone that scripts/build.ps1 expects; see README.md.
pin:
    python3 scripts/verify-pin.py

# Lint and run the AI-slop gate.
verify: lint aislop


# Prune remote-tracking refs and delete local branches merged into main.
prune:
    node scripts/prune.mjs