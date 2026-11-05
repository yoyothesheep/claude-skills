#!/usr/bin/env python3
"""Generate each agent's guardrail config from one neutral file, `.agent/guardrails.json`.

Run by a human at project setup (the generated files are themselves protected from the agent).
Safe to re-run: it merges into existing files and never removes your own settings.

Outputs:
- .claude/settings.json      permission deny rules + PreToolUse hook (merged)
- .claude/hooks/guard.py     the hook (copied from templates/guardrails/)
- .claude/agents/loop-*.md   role subagents (maker, verifier, scribe), each with the model for its tier from CONFIG.md;
                             the verifiers are read-only and CONFIG.md test/lint commands go to `verifier_bash_allow`
- .codex/agents/loop_*.toml  the same roles for Codex, when CONFIG.md sets CODEX_MODELS
- .gitignore                 secret and private-data paths (managed block)
- .cursorignore, .geminiignore   secret paths (managed block)
- AGENTS.md                  plain-language rules for agents without hooks, and the model roles (managed blocks)
- .git/hooks/pre-commit      with --git-hook: runs `check_loop.py guardrails` for any agent

Usage:
    python gen_guardrails.py --init [--git-hook] [--root PATH]   # copy the default config, then generate
    python gen_guardrails.py [--git-hook] [--root PATH]          # regenerate from the existing config
"""

from __future__ import annotations

import json
import re
import shutil
import stat
import sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "templates" / "guardrails"
HOOK_COMMAND = 'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard.py"'
HOOK_MATCHER = "Bash|Read|Edit|Write|MultiEdit|NotebookEdit"

# (agent name, template, CONFIG.md key for its tier, default tier, description suffix)
ROLES = [
    ("loop-maker", "loop-maker.md", "MAKER_TIER", "mid", " Low- and medium-risk units."),
    ("loop-maker-high", "loop-maker.md", "MAKER_TIER_HIGH_RISK", "top", " High-risk units."),
    ("loop-verifier", "loop-verifier.md", "VERIFIER_TIER", "mid", " Low-risk units."),
    ("loop-verifier-strict", "loop-verifier.md", "VERIFIER_TIER_STRICT", "top", " Medium- and high-risk units."),
    ("loop-scribe", "loop-scribe.md", "SCRIBE_TIER", "small", ""),
]
DEFAULT_CLAUDE_MODELS = "top=opus, mid=sonnet, small=haiku"
CODEX_EFFORT = {"top": "high", "mid": "medium", "small": "low"}


def rule_path(glob: str) -> str:
    return glob if glob.startswith(("**/", "/", "./")) else f"./{glob}"


def write_block(path: Path, body: str, start: str, end: str) -> None:
    """Replace the managed block in `path`, or append it. Content outside the markers is kept."""
    block = f"{start}\n{body.rstrip()}\n{end}"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    text = pattern.sub(lambda _: block, text) if pattern.search(text) else (text.rstrip() + "\n\n" if text.strip() else "") + block
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def gen_claude(root: Path, cfg: dict) -> None:
    settings_path = root / ".claude" / "settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8")) if settings_path.is_file() else {}
    wanted = (
        [f"Read({rule_path(g)})" for g in cfg.get("secret_paths", [])]
        + [f"Edit({rule_path(g)})" for g in cfg.get("protected_paths", [])]
        + [f"Bash({p}:*)" for p in cfg.get("denied_bash_prefixes", [])]
    )
    deny = settings.setdefault("permissions", {}).setdefault("deny", [])
    deny.extend(r for r in wanted if r not in deny)

    pre = settings.setdefault("hooks", {}).setdefault("PreToolUse", [])
    if not any("hooks/guard.py" in h.get("command", "") for e in pre for h in e.get("hooks", [])):
        pre.append({"matcher": HOOK_MATCHER, "hooks": [{"type": "command", "command": HOOK_COMMAND}]})

    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    hook = root / ".claude" / "hooks" / "guard.py"
    hook.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(TEMPLATES / "guard.py", hook)
    hook.chmod(hook.stat().st_mode | stat.S_IXUSR)


def read_config(root: Path) -> dict[str, str]:
    """`KEY: value` lines from the repo's CONFIG.md (root first, then the skill folder)."""
    for path in (root / "CONFIG.md", *(root / b / "skills" / "product-engineering" / "CONFIG.md" for b in (".agent", ".claude"))):
        if path.is_file():
            pairs = re.findall(r"^([A-Z][A-Z0-9_]*):[ \t]*(.*)$", path.read_text(encoding="utf-8"), re.MULTILINE)
            return {k: v.strip() for k, v in pairs}
    return {}


def config_commands(root: Path) -> list[str]:
    """TEST/LINT/FORMAT commands from the repo's CONFIG.md, which the verifier may run."""
    conf = read_config(root)
    return [conf[k] for k in ("TEST_COMMAND", "LINT_COMMAND", "FORMAT_COMMAND") if conf.get(k)]


def parse_models(spec: str) -> dict[str, str]:
    """`top=opus, mid=sonnet, small=haiku` -> {"top": "opus", ...}."""
    pairs = (item.split("=", 1) for item in spec.split(",") if "=" in item)
    return {k.strip(): v.strip() for k, v in pairs if k.strip() and v.strip()}


def split_template(name: str) -> tuple[dict[str, str], str]:
    _, front, body = (TEMPLATES / name).read_text(encoding="utf-8").split("---\n", 2)
    meta = dict(line.split(": ", 1) for line in front.strip().splitlines())
    return meta, body.strip()


def role_tiers(conf: dict[str, str]) -> list[tuple[str, str, str, dict[str, str], str]]:
    """(name, tier, description, frontmatter, body) for every role, tiers from CONFIG.md."""
    out = []
    for name, template, key, default, note in ROLES:
        meta, body = split_template(template)
        meta["name"] = name
        meta["description"] = meta["description"] + note
        out.append((name, conf.get(key) or default, meta["description"], meta, body))
    return out


def toml_multiline(text: str) -> str:
    return '"""\n' + text.replace("\\", "\\\\").replace('"""', '\\"""') + '\n"""'


def gen_agents(root: Path, conf: dict[str, str]) -> list[str]:
    """Role subagents for Claude Code, and for Codex when CODEX_MODELS is set. Returns warnings."""
    warnings = []
    claude = parse_models(conf.get("CLAUDE_MODELS") or DEFAULT_CLAUDE_MODELS)
    codex = parse_models(conf.get("CODEX_MODELS", ""))
    for name, tier, desc, meta, body in role_tiers(conf):
        for harness, models in (("CLAUDE_MODELS", claude), ("CODEX_MODELS", codex)):
            if models and tier not in models:
                warnings.append(f"{name}: tier '{tier}' not in {harness}; the agent inherits the session model")
        lines = ["---", *(f"{k}: {v}" for k, v in meta.items())]
        if tier in claude:
            lines.append(f"model: {claude[tier]}")
        path = root / ".claude" / "agents" / f"{name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join([*lines, "---", "", body, ""]), encoding="utf-8")
        if codex:
            toml = [f"name = {json.dumps(name.replace('-', '_'), ensure_ascii=False)}",
                    f"description = {json.dumps(desc, ensure_ascii=False)}"]
            if tier in codex:
                toml += [f"model = {json.dumps(codex[tier])}", f"model_reasoning_effort = {json.dumps(CODEX_EFFORT.get(tier, 'medium'))}"]
            toml.append(f"developer_instructions = {toml_multiline(body)}")
            path = root / ".codex" / "agents" / f"{name.replace('-', '_')}.toml"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("\n".join(toml) + "\n", encoding="utf-8")
    return warnings


def gen_roles_md(root: Path, conf: dict[str, str]) -> None:
    claude = parse_models(conf.get("CLAUDE_MODELS") or DEFAULT_CLAUDE_MODELS)
    codex = parse_models(conf.get("CODEX_MODELS", ""))
    planner = conf.get("PLANNER_TIER") or "top"
    phases = {"loop-maker": "3–4", "loop-maker-high": "3–4 (high risk)", "loop-verifier": "5 (low risk)",
              "loop-verifier-strict": "5 (medium/high risk)", "loop-scribe": "6"}
    model = lambda m, t: m.get(t, "session model")
    lines = [
        "## Model roles (product-engineering)",
        "",
        "Roles map to tiers in `CONFIG.md`; tiers map to each tool's models. Where a tool can't route a role to its model, run that phase in a fresh session on the listed model.",
        "",
        "| Role | Phases | Tier | Claude Code | Codex |",
        "|:---|:---|:---|:---|:---|",
        f"| planner (main session) | 0–2, orchestration | {planner} | {model(claude, planner)} | {model(codex, planner)} |",
    ]
    for name, tier, *_ in role_tiers(conf):
        lines.append(f"| `{name}` | {phases[name]} | {tier} | {model(claude, tier)} | {model(codex, tier)} |")
    write_block(root / "AGENTS.md", "\n".join(lines), "<!-- roles:start -->", "<!-- roles:end -->")


def gen_ignore_files(root: Path, cfg: dict) -> None:
    body = "\n".join(cfg.get("secret_paths", []))
    for name in (".cursorignore", ".geminiignore"):
        write_block(root / name, body, "# guardrails:start", "# guardrails:end")


def gen_gitignore(root: Path, cfg: dict) -> None:
    allow = cfg.get("private_data_allow", [])
    lines = cfg.get("secret_paths", []) + cfg.get("private_data_paths", [])
    lines += [f"!{a.rstrip('*').rstrip('/')}/**/{g.split('/')[-1]}" for a in allow for g in cfg.get("private_data_paths", []) if g.startswith("**/*.")]
    write_block(root / ".gitignore", "\n".join(lines), "# guardrails:start", "# guardrails:end")


def gen_agents_md(root: Path, cfg: dict) -> None:
    lines = [
        "## Guardrails",
        "",
        "Rules from `.agent/guardrails.json`. Hooks enforce them where the agent supports hooks; follow them everywhere.",
        "",
        "- Never read or write: " + ", ".join(f"`{g}`" for g in cfg.get("secret_paths", [])),
        "- Never edit (change by hand and record an ADR): " + ", ".join(f"`{g}`" for g in cfg.get("protected_paths", [])),
        "- Append-only (add new files, never edit existing): " + ", ".join(f"`{g}`" for g in cfg.get("append_only_paths", [])),
        "- Never commit user data: " + ", ".join(f"`{g}`" for g in cfg.get("private_data_paths", [])) + " (allowed only in " + ", ".join(f"`{a}`" for a in cfg.get("private_data_allow", [])) + ")",
        "- Test data is synthetic: fake names, `example.com` emails, test card numbers. Never copy real user records into fixtures.",
        "- If a secret is ever committed, rotate it. Removing it from history does not un-leak it.",
        "- Changes need a new ADR in `history/decisions/` (design system): " + ", ".join(f"`{g}`" for g in cfg.get("adr_required_paths", [])),
        "- Never run: " + ", ".join(f"`{p}`" for p in cfg.get("denied_bash_prefixes", [])) + ", `DROP TABLE`, `curl | sh`",
    ]
    write_block(root / "AGENTS.md", "\n".join(lines), "<!-- guardrails:start -->", "<!-- guardrails:end -->")


def gen_git_hook(root: Path) -> str:
    hooks = root / ".git" / "hooks"
    if not hooks.is_dir():
        return "skipped: no .git/hooks directory"
    target = hooks / "pre-commit"
    if target.exists():
        return "skipped: .git/hooks/pre-commit already exists; add `check_loop.py guardrails` to it by hand"
    checker = root / ".agent" / "skills" / "product-engineering" / "scripts" / "check_loop.py"
    checker = checker if checker.is_file() else Path(__file__).resolve().parent / "check_loop.py"
    target.write_text(f'#!/bin/sh\npython3 "{checker}" guardrails > /dev/null || {{ echo "Guardrail check failed; run: python3 {checker} guardrails"; exit 1; }}\n', encoding="utf-8")
    target.chmod(target.stat().st_mode | stat.S_IXUSR)
    return "installed .git/hooks/pre-commit"


def main(argv: list[str]) -> int:
    root = Path.cwd()
    if "--root" in argv:
        root = Path(argv[argv.index("--root") + 1])
    root = root.resolve()
    cfg_path = root / ".agent" / "guardrails.json"

    if "--init" in argv and not cfg_path.is_file():
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(TEMPLATES / "guardrails.json", cfg_path)
        print(f"created {cfg_path.relative_to(root)}")
    if not cfg_path.is_file():
        print("No .agent/guardrails.json. Run with --init to create it.", file=sys.stderr)
        return 1

    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    allow = cfg.setdefault("verifier_bash_allow", [])
    new = [c for c in config_commands(root) if c not in allow]
    if new:
        allow.extend(new)
        cfg_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    conf = read_config(root)
    gen_claude(root, cfg)
    warnings = gen_agents(root, conf)
    gen_ignore_files(root, cfg)
    gen_gitignore(root, cfg)
    gen_agents_md(root, cfg)
    gen_roles_md(root, conf)
    codex = ", .codex/agents/loop_*.toml" if conf.get("CODEX_MODELS") else ""
    print(f"wrote .claude/settings.json, .claude/hooks/guard.py, .claude/agents/loop-*.md{codex}, .gitignore, .cursorignore, .geminiignore, AGENTS.md")
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if "--git-hook" in argv:
        print(gen_git_hook(root))
    print("Next: write the baseline guardrails ADR (templates/GUARDRAILS_ADR_TEMPLATE.md) and cite it from the skeleton unit.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
