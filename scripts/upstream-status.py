#!/usr/bin/env python3
"""Report upstream drift for the pinned sources of truth.

Read pstack.lock.json and NOTICE-port.md, fetch the pinned pstack-claude
repository and cursor/plugins, and report the commits and changed files this
OpenCode port has not absorbed. Exit 0 when the pin is current, 1 when
upstream has moved, and 2 on an operational error.

Uses only the Python standard library and git. Paths resolve from the
environment, so it runs on Windows and macOS with no hardcoded drives.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys

DEFAULT_CURSOR_REPOSITORY = "https://github.com/cursor/plugins.git"
DEFAULT_CURSOR_PATH = "pstack"


class GitError(RuntimeError):
    pass


def git(args, cwd=None, check=True):
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
    )
    if check and proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise GitError("git " + " ".join(args) + ": " + detail)
    return proc.stdout.strip()


def data_home():
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or os.path.join(pathlib.Path.home(), "AppData", "Local")
    else:
        base = os.environ.get("XDG_DATA_HOME") or os.path.join(pathlib.Path.home(), ".local", "share")
    return pathlib.Path(base) / "maxstack"


def default_cache(name):
    return data_home() / "upstream-status" / name


def remote_head(url):
    out = git(["ls-remote", "--symref", url, "HEAD"])
    sha = None
    ref = None
    for line in out.splitlines():
        if line.startswith("ref:"):
            ref = line.split()[1]
        elif line.endswith("\tHEAD"):
            sha = line.split("\t", 1)[0]
    if not sha:
        raise GitError("could not read HEAD from " + url)
    return sha, ref


def ensure_clone(path, url):
    path = pathlib.Path(path)
    if (path / ".git").is_dir():
        git(["-C", str(path), "fetch", "--quiet", "--prune", "origin"])
    else:
        if path.exists():
            raise GitError(str(path) + " exists but is not a git clone")
        path.parent.mkdir(parents=True, exist_ok=True)
        git(["clone", "--quiet", "--filter=blob:none", url, str(path)])
    return path


def has_commit(repo, sha):
    proc = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", sha + "^{commit}"],
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0


def rev_parse(repo, sha):
    return git(["-C", str(repo), "rev-parse", sha + "^{commit}"])


def resolve_commit(repo, sha):
    return rev_parse(repo, sha) if has_commit(repo, sha) else None


def short_log(repo, base, head, limit):
    args = ["-C", str(repo), "log", "--no-decorate", "-n" + str(limit), "--format=%h %s", base + ".." + head]
    return [line for line in git(args).splitlines() if line.strip()]


def changed_files(repo, base, head, path=None):
    args = ["-C", str(repo), "diff", "--name-status", base, head]
    if path:
        args += ["--", path]
    return [line for line in git(args).splitlines() if line.strip()]


def commit_time(repo, sha):
    return int(git(["-C", str(repo), "show", "-s", "--format=%ct", sha]) or 0)


def cursor_commit_candidates(text):
    candidates = []
    for pattern in (
        r"cursor/plugins[^\s\]]*@\s*([0-9a-f]{7,40})",
        r"cursor/plugins/tree/([0-9a-f]{7,40})",
    ):
        candidates.extend(re.findall(pattern, text))
    return candidates


def newest_absorbed(repo, text):
    resolved = []
    for candidate in cursor_commit_candidates(text):
        full = resolve_commit(repo, candidate)
        if full:
            resolved.append((commit_time(repo, full), full))
    return max(resolved)[1] if resolved else None


def print_section(title, commits, files, prefix):
    print("[{}] {} commit(s) and {} changed file(s) past {}:".format(title, len(commits), len(files), prefix))
    for line in commits:
        print("  " + line)
    for line in files:
        print("  " + line)


def report_pin(repository, pin_commit, clone, limit):
    """Print the pstack-claude section. Return drift, or None when the check cannot run."""
    print("pinned repository: " + repository)
    print("pinned commit:     " + pin_commit)
    try:
        head_sha, head_ref = remote_head(repository)
        print("upstream HEAD:     " + head_sha + (" (" + head_ref + ")" if head_ref else ""))
        repo = ensure_clone(clone, repository)
        if not has_commit(repo, pin_commit):
            print("WARNING: pinned commit is not reachable in the clone; history may be rewritten", file=sys.stderr)
            return None
        pin_full = rev_parse(repo, pin_commit)
        if head_sha == pin_full:
            print("[pstack-claude] up to date with the pin.")
            return False
        commits = short_log(repo, pin_full, head_sha, limit)
        files = changed_files(repo, pin_full, head_sha)
        print_section("pstack-claude", commits, files, "the pin " + pin_full[:12])
        return True
    except GitError as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return None


def report_cursor(repository, path, absorbed, clone, notice_text, limit):
    """Print the cursor/plugins section. Return drift, or None when the check cannot run."""
    try:
        repo = ensure_clone(clone, repository)
        notice_absorbed = newest_absorbed(repo, notice_text)
        source = absorbed or notice_absorbed
        if not source:
            print("[cursor/plugins] WARNING: no absorbed Cursor commit recorded; skipping.", file=sys.stderr)
            return None
        absorbed_full = resolve_commit(repo, source)
        if not absorbed_full:
            print("[cursor/plugins] WARNING: absorbed commit " + source + " is not in the clone.", file=sys.stderr)
            return None
        if notice_absorbed and absorbed_full != notice_absorbed:
            print(
                "[cursor/plugins] WARNING: lock records " + absorbed_full[:12]
                + " but NOTICE-port.md cites " + notice_absorbed[:12],
                file=sys.stderr,
            )
        head_sha, _ = remote_head(repository)
        print("[cursor/plugins] absorbed " + absorbed_full[:12] + ", HEAD " + head_sha[:12])
        if head_sha == absorbed_full:
            print("[cursor/plugins] up to date under " + path + "/.")
            return False
        commits = short_log(repo, absorbed_full, head_sha, limit)
        files = changed_files(repo, absorbed_full, head_sha, path)
        print_section("cursor/plugins", commits, files, "the absorbed commit " + absorbed_full[:12])
        return True
    except GitError as exc:
        print("[cursor/plugins] WARNING: check skipped: " + str(exc), file=sys.stderr)
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(description="Report upstream pstack drift against pstack.lock.json.")
    parser.add_argument("--lock", default="pstack.lock.json", help="path to pstack.lock.json")
    parser.add_argument("--notice", default="NOTICE-port.md", help="path to NOTICE-port.md")
    parser.add_argument("--repository", help="override the pinned repository URL")
    parser.add_argument("--commit", help="override the pinned commit")
    parser.add_argument("--clone", help="cache clone for the pinned repository")
    parser.add_argument("--cursor-repository", help="override the cursor/plugins repository URL")
    parser.add_argument("--cursor-path", help="path inside cursor/plugins to watch")
    parser.add_argument("--cursor-commit", help="override the absorbed Cursor commit")
    parser.add_argument("--cursor-clone", help="cache clone for cursor/plugins")
    parser.add_argument("--no-cursor", action="store_true", help="skip the cursor/plugins check")
    parser.add_argument("--max-commits", type=int, default=20, help="commits to list per source")
    args = parser.parse_args(argv)

    lock_path = pathlib.Path(args.lock)
    lock = json.loads(lock_path.read_text(encoding="utf-8")) if lock_path.is_file() else {}
    port_of = lock.get("portOf") if isinstance(lock.get("portOf"), dict) else {}

    repository = args.repository or lock.get("repository")
    pin_commit = args.commit or lock.get("commit")
    if not repository or not pin_commit:
        print("ERROR: repository and commit must come from pstack.lock.json or the flags", file=sys.stderr)
        return 2

    clone = pathlib.Path(args.clone) if args.clone else default_cache("pstack-claude")
    notice_path = pathlib.Path(args.notice)
    notice_text = notice_path.read_text(encoding="utf-8") if notice_path.is_file() else ""

    print("== pstack upstream status ==")
    pin_drift = report_pin(repository, pin_commit, clone, args.max_commits)
    if pin_drift is None:
        print("RESULT: cannot compare pstack-claude.")
        return 2

    drift = pin_drift
    if not args.no_cursor:
        cursor_drift = report_cursor(
            args.cursor_repository or port_of.get("repository") or DEFAULT_CURSOR_REPOSITORY,
            args.cursor_path or port_of.get("path") or DEFAULT_CURSOR_PATH,
            args.cursor_commit or port_of.get("absorbedCommit"),
            pathlib.Path(args.cursor_clone) if args.cursor_clone else default_cache("cursor-plugins"),
            notice_text,
            args.max_commits,
        )
        drift = drift or bool(cursor_drift)

    print()
    if drift:
        print("RESULT: upstream has changes this port has not absorbed.")
        return 1
    print("RESULT: the pin and the absorbed Cursor commit are current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
