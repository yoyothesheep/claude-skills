#!/usr/bin/env python3
"""Deterministic repo scan for the `product-launch-audit` skill.

Works on any folder (git repo or not). Emits JSON evidence; the LLM layer turns it
into the pillar report. Statuses: pass | warn | fail | manual (a human must check).

Usage:
    python audit_repo.py [path]     # default: current directory
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".next", ".expo", "coverage"}
SKIP_FILES = re.compile(r"(package-lock\.json|yarn\.lock|pnpm-lock\.yaml|uv\.lock|poetry\.lock|\.min\.js|\.map)$")
CODE_EXTS = (".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".json", ".yml", ".yaml", ".toml", ".env", ".sql", ".sh", ".md", ".txt")
TEMPLATE_ENV = re.compile(r"\.(example|sample|template|dist)$")

SECRET_RES = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{16,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"(?i)(?:api[_-]?key|secret|token|passwd|password|service[_-]?role)\w*\s*[:=]\s*['\"][A-Za-z0-9_\-./+=]{16,}['\"]"),
]
SECRET_IGNORE = re.compile(r"(?i)process\.env|os\.environ|getenv|import\.meta\.env|example|your[_-]|xxx|changeme|placeholder|<[^>]+>|\$\{")

ROUTE_RE = re.compile(
    r"\b(?:app|router|api)\.(?:get|post|put|patch|delete|all)\(|@(?:app|router|api)\.(?:get|post|put|patch|delete)\(|"
    r"export\s+(?:async\s+)?function\s+(?:GET|POST|PUT|PATCH|DELETE)\b"
)
AUTH_RE = re.compile(
    r"(?i)auth|session|getUser|currentUser|clerk|jwt|verify_token|Depends\(|login_required|requireUser|bearer|middleware"
)

DEP_FILES = ("package.json", "requirements.txt", "pyproject.toml", "Pipfile", "go.mod", "Gemfile")
ERROR_TRACKERS = ("sentry", "bugsnag", "rollbar", "honeybadger", "datadog", "logrocket", "highlight.run")
RATE_LIMITERS = ("express-rate-limit", "rate-limiter-flexible", "@upstash/ratelimit", "slowapi", "flask-limiter", "django-ratelimit", "fastapi-limiter", "rate_limit", "ratelimit")
LOCKFILES = ("package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "uv.lock", "poetry.lock", "Pipfile.lock", "go.sum", "Gemfile.lock")


def git(root: Path, *args: str) -> tuple[int, str]:
    try:
        p = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=60)
        return p.returncode, p.stdout.strip()
    except Exception as e:
        return 1, str(e)


def list_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not SKIP_FILES.search(f):
                out.append(Path(dirpath, f))
    return out


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def check(pillar: str, cid: str, status: str, detail: str, **extra) -> dict:
    return {"pillar": pillar, "id": cid, "status": status, "detail": detail, **extra}


def scan_secrets(root: Path, files: list[Path]) -> list[dict]:
    hits = []
    for p in files:
        name = p.name
        if not (name.endswith(CODE_EXTS) or name.startswith(".env")) or TEMPLATE_ENV.search(name):
            continue
        for n, line in enumerate(read(p).splitlines(), 1):
            if len(line) > 400 or SECRET_IGNORE.search(line):
                continue
            if any(r.search(line) for r in SECRET_RES):
                hits.append({"file": str(p.relative_to(root)), "line": n})
                break
    return hits


def scan_endpoints(root: Path, files: list[Path]) -> list[str]:
    """Files that define routes but mention no auth at all. A heuristic: review each one."""
    flagged = []
    for p in files:
        if not p.name.endswith((".py", ".ts", ".tsx", ".js", ".jsx", ".mjs")) or re.search(r"\.(test|spec)\.|test_", p.name):
            continue
        text = read(p)
        if ROUTE_RE.search(text) and not AUTH_RE.search(text):
            flagged.append(str(p.relative_to(root)))
    return flagged


def rls_gaps(files: list[Path]) -> tuple[int, list[str]]:
    created, secured = set(), set()
    for p in files:
        if p.suffix != ".sql":
            continue
        text = read(p).lower()
        created |= set(re.findall(r"create table (?:if not exists )?(?:public\.)?\"?(\w+)\"?", text))
        secured |= set(re.findall(r"alter table (?:only )?(?:public\.)?\"?(\w+)\"? enable row level security", text))
    return len(created), sorted(created - secured)


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    files = list_files(root)
    rel = lambda p: str(p.relative_to(root))
    checks: list[dict] = []

    # Pillar 1: infrastructure and hosting
    is_git = git(root, "rev-parse", "--is-inside-work-tree")[0] == 0
    if not is_git:
        checks.append(check("infra", "git_repo", "fail", "Not a git repo. Code exists only in the tool's history or local disk."))
    else:
        has_commits = git(root, "rev-parse", "HEAD")[0] == 0
        _, remotes = git(root, "remote")
        checks.append(check("infra", "git_repo", "pass" if has_commits else "warn", "Git repo" + ("" if has_commits else " with no commits")))
        checks.append(check("infra", "git_remote", "pass" if remotes else "fail", f"Remotes: {remotes or 'none (no off-machine backup)'}"))

    env_files = [rel(p) for p in files if re.match(r"\.env(\..+)?$", p.name) and not TEMPLATE_ENV.search(p.name)]
    gitignore = read(root / ".gitignore")
    ignores_env = bool(re.search(r"^\.env\b", gitignore, re.MULTILINE))
    tracked_env = []
    if is_git and env_files:
        _, tracked = git(root, "ls-files", "--", *env_files)
        tracked_env = tracked.splitlines()
    if tracked_env:
        checks.append(check("infra", "env_committed", "fail", "Env files tracked by git", files=tracked_env))
    elif env_files and not ignores_env:
        checks.append(check("infra", "env_ignored", "fail", ".env present but not in .gitignore", files=env_files))
    else:
        checks.append(check("infra", "env_committed", "pass", "No tracked .env files"))

    checks.append(check("infra", "ci", "pass" if (root / ".github" / "workflows").is_dir() else "warn", "CI workflows " + ("found" if (root / ".github" / "workflows").is_dir() else "not found")))
    for cid, q in (("staging", "Is there a staging environment before production?"),
                   ("hosting_defaults", "Hosting tier: dedicated or cold-start? Database backups on?"),
                   ("agent_permissions", "What can the AI agent read, write and delete?")):
        checks.append(check("infra", cid, "manual", q))

    # Pillar 2: code quality and testing
    tests = [rel(p) for p in files if re.search(r"(^test_|\.test\.|\.spec\.)", p.name) or "/tests/" in "/" + rel(p)]
    checks.append(check("quality", "tests_exist", "pass" if tests else "fail", f"{len(tests)} test file(s)", sample=tests[:5]))
    checks.append(check("quality", "critical_flow_covered", "manual", "Does at least one test cover the critical user flow?"))

    # Pillar 3: security and data
    secrets = scan_secrets(root, files)
    checks.append(check("security", "secrets_in_source", "fail" if secrets else "pass", f"{len(secrets)} file(s) with likely secrets" if secrets else "No likely secrets found", hits=secrets[:20]))
    flagged = scan_endpoints(root, files)
    checks.append(check("security", "endpoints_without_auth", "warn" if flagged else "pass",
                        "Heuristic: these files define routes and mention no auth. Review each." if flagged else "Every route file mentions auth", files=flagged[:30]))
    uses_supabase = any("supabase" in read(p).lower() for p in files if p.name in DEP_FILES) or (root / "supabase").is_dir()
    if uses_supabase:
        n, gaps = rls_gaps(files)
        if n == 0:
            checks.append(check("security", "rls", "manual", "Supabase in use but no CREATE TABLE in SQL files. Check RLS in the dashboard."))
        else:
            checks.append(check("security", "rls", "fail" if gaps else "pass", f"{len(gaps)} of {n} table(s) without RLS" if gaps else f"RLS enabled on all {n} tables", tables=gaps))
    lock = [l for l in LOCKFILES if (root / l).exists()]
    has_deps = any((root / d).exists() for d in DEP_FILES)
    if has_deps:
        checks.append(check("security", "lockfile", "pass" if lock else "warn", f"Lockfile: {lock[0]}" if lock else "No lockfile; installs are not reproducible"))
        checks.append(check("security", "dependency_audit", "manual", "Run `npm audit` / `pip-audit` and review what the AI pulled in."))
    checks.append(check("security", "ai_data_handling", "manual", "What customer data reaches third-party AI tools?"))

    # Pillars 4 and 3: observability, cost, rate limits
    dep_text = " ".join(read(root / d).lower() for d in DEP_FILES)
    tracker = [t for t in ERROR_TRACKERS if t in dep_text]
    checks.append(check("observability", "error_tracker", "pass" if tracker else "fail", f"Found: {', '.join(tracker)}" if tracker else "No error tracker dependency"))
    limiter = [r for r in RATE_LIMITERS if r in dep_text]
    checks.append(check("infra", "rate_limit", "pass" if limiter else "warn", f"Found: {', '.join(limiter)}" if limiter else "No rate-limit dependency (may be handled by the host)"))
    checks.append(check("observability", "monthly_cost", "manual", "Add up hosting, database and AI/API spend. Is a spend cap set on the model provider?"))

    # Pillar 5: failure and rollback
    checks.append(check("rollback", "rollback_dry_run", "manual", "Has anyone done a rollback dry run?"))
    checks.append(check("rollback", "runbook", "manual", "Is there a runbook: who to call, what to check first, what to do on a data breach?"))

    counts = {s: sum(c["status"] == s for c in checks) for s in ("pass", "warn", "fail", "manual")}
    print(json.dumps({"root": str(root), "counts": counts, "checks": checks}, indent=2))
    return 1 if counts["fail"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
