#!/usr/bin/env python3
"""Pre-tool hook for Claude Code, Cursor and Codex. Enforces .agent/guardrails.json; exit 2 blocks the call.

Installed to .claude/hooks/guard.py by scripts/gen_guardrails.py and registered in .claude/settings.json,
.cursor/hooks.json (preToolUse, beforeReadFile) and .codex/hooks.json (PreToolUse). Each harness's
event is normalized to Claude Code's tool names first. Blocks only what git can't undo:
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

# The hook lives at <repo>/.claude/hooks/guard.py. Trust that over the environment: Cursor aliases
# CLAUDE_PROJECT_DIR, Codex sets no project variable, and either may run from a subdirectory.
_HOME = Path(__file__).resolve().parents[2]
ROOT = _HOME if (_HOME / ".agent").is_dir() else Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()
CURSOR_TOOLS = {"Shell": "Bash", "Read": "Read", "Write": "Write", "Edit": "Edit", "Delete": "Write", "StrReplace": "Edit"}
PATH_KEYS = ("file_path", "notebook_path", "path", "target_file", "filePath")
PATCH_PATH = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$|^\*\*\* Move to: (.+)$", re.MULTILINE)
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


def path_arg(args: dict) -> str:
    return next((str(args[k]) for k in PATH_KEYS if args.get(k)), "")


def normalize(event: dict) -> list[tuple[str, dict]]:
    """Each harness's event as Claude Code (tool, args) calls; a Codex patch becomes one Write per file."""
    name, args = event.get("hook_event_name", ""), event.get("tool_input") or {}
    if name == "beforeReadFile":
        return [("Read", {"file_path": event.get("file_path", "")})]
    if name == "preToolUse":
        tool = CURSOR_TOOLS.get(event.get("tool_name", ""), "")
        return [(tool, {"command": args.get("command", "")} if tool == "Bash" else {"file_path": path_arg(args)})] if tool else []
    if event.get("tool_name") == "apply_patch":
        patch = next((v for v in args.values() if isinstance(v, str) and "*** " in v), "")
        base = Path(event.get("cwd") or ROOT)
        return [("Write", {"file_path": str(base / (a or b).strip())}) for a, b in PATCH_PATH.findall(patch)] or [("Write", {})]
    return [(event.get("tool_name", ""), {**args, "file_path": path_arg(args)} if path_arg(args) else args)]


def is_verifier(event: dict) -> bool:
    return str(event.get("agent_type") or "").replace("_", "-").startswith(VERIFIER)


def decide(event: dict, cfg: dict) -> str | None:
    for tool, args in normalize(event):
        reason = check(cfg, tool, args) or (verifier_check(cfg, tool, args) if is_verifier(event) else None)
        if reason:
            return reason
    return None


def main() -> int:
    cfg_path = ROOT / ".agent" / "guardrails.json"
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}
    cursor = "cursor_version" in event
    try:
        reason = decide(event, json.loads(cfg_path.read_text(encoding="utf-8"))) if cfg_path.is_file() else None
    except (ValueError, OSError):
        reason = None
    if reason:
        print(f"Blocked by guardrails: {reason}", file=sys.stderr)
        if cursor:
            print(json.dumps({"permission": "deny", "user_message": f"Blocked by guardrails: {reason}", "agent_message": f"Blocked by guardrails: {reason}"}))
        return 2
    if cursor:  # Cursor treats empty output from a permission hook as invalid and blocks
        print(json.dumps({"permission": "allow"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
