# product-engineering configuration

# Directory paths (relative to repository root)
ACTIVE_DIR: active
SPECS_DIR: specs
PRODUCT_SPECS_DIR: specs/product
ENGINEERING_SPECS_DIR: specs/engineering
DECISIONS_DIR: history/decisions
COMPLETED_MILESTONES_DIR: history/milestones
TESTS_DIR: tests

# Living documentation files
LIVING_SPEC: specs/README.md
WORKING_RULES: CLAUDE.md

# Command configurations. TEST_COMMAND runs every automated tier: unit, integration, end-to-end, and
# free live tests (they skip-and-report without their dev key). Paid live checks are manual [Live] walkthroughs.
TEST_COMMAND: uv run pytest
# Hosts free live tests may reach; every other outbound connection is blocked in tests. Free dev/sandbox
# services only (analytics ingestion + its query API). Never a paid service (LLM, SMS, paid APIs).
LIVE_ALLOWED_HOSTS: api.mixpanel.com, api-js.mixpanel.com, mixpanel.com
LINT_COMMAND: uv run ruff check .
FORMAT_COMMAND: uv run ruff format --check .

# UI verification viewports (px, widest first; optional). Every UI unit is checked at EACH width,
# not one desktop + one phone sample. Automated tests assert no horizontal overflow at every width;
# responsive M scenarios name the widths they check.
VIEWPORT_BREAKPOINTS: 1440, 1280, 991, 767, 479, 375
# Reference site for visual parity (blank if none). Parity = measured element boxes (position, size,
# font-size) of key elements (title, lead, hero media, nav, dividers) match the reference at every
# width; any difference over ~10px or any font-size mismatch is a finding. Read the reference's CSS
# min-width/max-width media queries so wide-screen tiers aren't missed.
PARITY_REFERENCE_URL: 

# Analytics (in-app events & session replay via posthog or mixpanel; traffic acquisition via google-analytics).
# Separate dev and prod projects, each with its own key in env; a human creates them in Phase 0.
ANALYTICS_PLATFORM: mixpanel
# How the agent reaches it: an MCP server name or an API base URL (keys stay in env, never here)
ANALYTICS_ACCESS: mcp:mixpanel
ACQUISITION_ANALYTICS: google-analytics
# The event catalogue the skeleton creates: every event name with its required properties (see SKILL.md, Analytics test kit).
ANALYTICS_CATALOGUE: app/analytics_events.py

# Model routing. Each role runs at a tier; each tool maps tiers to its models.
# Planning (Phases 1–2) and orchestration run in the main session: start it on the PLANNER_TIER model.
# Phases 3–4 go to loop-maker, Phase 5 to loop-verifier, Phase 6 to loop-scribe (scripts/gen_guardrails.py
# writes each with its model). Re-run gen_guardrails.py after changing any of these.
PLANNER_TIER: top
MAKER_TIER: mid
MAKER_TIER_HIGH_RISK: top
VERIFIER_TIER: mid
VERIFIER_TIER_STRICT: top
SCRIBE_TIER: small
# Tier -> model. Claude Code aliases track the latest version. Blank CODEX_MODELS to skip .codex/agents/ and .codex/hooks.json.
# CURSOR_MODELS takes model IDs from Cursor's model picker; blank means every role inherits the session model.
CLAUDE_MODELS: top=opus, mid=sonnet, small=haiku
CURSOR_MODELS:
CODEX_MODELS: top=gpt-6-astra, mid=gpt-6.1-sol, small=gpt-6-luna

# Invariants & Policy Flags
REQUIRE_MAKER_VERIFIER_SEPARATION: true
AUTO_COMMIT: false
DETERMINISTIC_LOGIC_ISOLATED: true

