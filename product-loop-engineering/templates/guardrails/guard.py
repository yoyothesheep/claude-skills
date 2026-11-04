#!/usr/bin/env python3
"""PreToolUse hook for Claude Code. Enforces .agent/guardrails.json; exit 2 blocks the call.

Installed to .claude/hooks/guard.py by scripts/gen_guardrails.py. Blocks only what git can't undo:
secret reads (they reach the model provider), edits to the guardrails themselves, and commands that
destroy uncommitted work or act outside the repo. Best-effort: a shell can dodge pattern checks,
so the credentials and sandbox are the real boundary.
"""

import fnmatch
import json
import os
import re
import shlex
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
WRITE_VERBS = re.compile(r"(?:^|[\s;&|])(?:rm|mv|truncate|tee|sed\s+-i\S*|chmod)\b|>>?")
VERIFIER = "loop-verifier"
VERIFIER_ALLOW = ("cd", "ls", "cat", "head", "tail", "wc", "grep", "rg", "git diff", "git log", "git show", "git status", "git ls-files", "git blame")
CHECKER_RE = re.compile(r"python3?\s+\S*check_loop\.py(?:\s|$)")
HARMLESS_REDIRECT = re.compile(r"\d?>&\d|\d?>\s*/dev/null")
SHELL_ESCAPE = re.compile(r">|\$\(|`|--output")


def verifier_check(cfg: dict, tool: str, args: dict) -> str | None:
    """The Phase 5 verifier reads and runs; it never writes. Bash is an allowlist, not a denylist."""
    if tool in WRITE_TOOLS:
        return "the verifier is read-only"
    if tool != "Bash":
        return None
    cmd = HARMLESS_REDIRECT.sub("", args.get("command", ""))
    if SHELL_ESCAPE.search(cmd):
        return "the verifier can't redirect output or run subshells"
    allow = [a.strip() for a in (*VERIFIER_ALLOW, *cfg.get("verifier_bash_allow", [])) if a.strip()]
    for seg in filter(None, (s.strip() for s in re.split(r"&&|\|\||[;|\n]", cmd))):
        if not CHECKER_RE.match(seg) and not any(seg == a or seg.startswith(a + " ") for a in allow):
            return f"the verifier may only run read-only commands, check_loop.py, and verifier_bash_allow; blocked: {seg[:80]}"
    return None


def matches(path: str, globs: list[str]) -> bool:
    for g in globs:
        for pat in {g, g[3:] if g.startswith("**/") else g}:
            if fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(os.path.basename(path), pat):
                return True
    return False


def relative(path: str) -> str:
    p = Path(path)
    p = p if p.is_absolute() else ROOT / p
    try:
        return str(p.resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def check(cfg: dict, tool: str, args: dict) -> str | None:
    secrets, protected = cfg.get("secret_paths", []), cfg.get("protected_paths", [])
    if tool == "Read":
        path = relative(args.get("file_path", ""))
        return f"{path} is a secret path; read it yourself and pass the value through the environment" if matches(path, secrets) else None
    if tool in WRITE_TOOLS:
        path = relative(args.get("file_path") or args.get("notebook_path") or "")
        if matches(path, secrets):
            return f"{path} is a secret path"
        if matches(path, protected):
            return f"{path} is guardrail config; change it by hand and record an ADR"
        return None
    if tool == "Bash":
        cmd = args.get("command", "")
        for pat in cfg.get("denied_bash_patterns", []):
            if re.search(pat, cmd, re.IGNORECASE):
                return f"command blocked by guardrail pattern {pat!r}"
        try:
            tokens = shlex.split(cmd)
        except ValueError:
            tokens = cmd.split()
        paths = [relative(t) for t in tokens if not t.startswith("-")]
        if any(matches(p, secrets) for p in paths):
            return "command touches a secret path"
        if WRITE_VERBS.search(cmd):
            for p in paths:
                if matches(p, protected):
                    return f"{p} is guardrail config; change it by hand and record an ADR"
    return None


def main() -> int:
    cfg_path = ROOT / ".agent" / "guardrails.json"
    if not cfg_path.is_file():
        return 0
    try:
        event = json.load(sys.stdin)
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return 0
    tool, args = event.get("tool_name", ""), event.get("tool_input") or {}
    reason = check(cfg, tool, args) or (verifier_check(cfg, tool, args) if event.get("agent_type") == VERIFIER else None)
    if reason:
        print(f"Blocked by guardrails: {reason}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
