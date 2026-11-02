# Loop Engineering Skill Configuration

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

# Command configurations
TEST_COMMAND: uv run pytest
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

# Analytics (events instrumented per unit; final reporting unit builds dashboards/queries here)
ANALYTICS_PLATFORM: posthog
# How the agent reaches it: an MCP server name or an API base URL (keys stay in env, never here)
ANALYTICS_ACCESS: mcp:posthog

# Invariants & Policy Flags
REQUIRE_MAKER_VERIFIER_SEPARATION: true
AUTO_COMMIT: false
DETERMINISTIC_LOGIC_ISOLATED: true

# Test cases & Workshop reference
TEST_CASES: tests/TEST_CASES.md
WORKSHOP_URL: https://luma.com/22i8vgcm
